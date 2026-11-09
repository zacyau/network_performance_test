"""网络性能测试工具 - 前后端不分离版本

FastAPI 单服务：服务端渲染页面（Jinja2 模板）+ 同源 API。
网络指标通过 curl 采集：耗时指标（DNS/TCP/SSL/首包/重定向/总耗时）
+ 请求详情（状态码、HTTP 版本、远端地址、下载大小与速度、内容类型、SSL 证书）。
"""

import re
import subprocess
from datetime import datetime, timezone

from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="网络性能测试工具")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# curl 输出格式：'|' 分隔，避免 content_type 中的逗号/分号干扰
CURL_WRITE_OUT = (
    "%{time_namelookup}|%{time_connect}|%{time_appconnect}|%{time_pretransfer}|"
    "%{time_starttransfer}|%{time_total}|%{http_code}|%{http_version}|"
    "%{remote_ip}|%{remote_port}|%{num_redirects}|%{time_redirect}|"
    "%{size_download}|%{speed_download}|%{content_type}"
)

CURL_TIMEOUT = 30


def _to_int(value, default=0):
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default


def _to_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def _last_line_match(keyword, text):
    """按行匹配关键字（兼容带/不带 '*' 前缀、任意缩进的 curl -v 输出），
    取最后一次匹配（重定向场景下对应最终连接）"""
    pattern = rf"^\s*\*?\s*{re.escape(keyword)}:\s*(.+)$"
    matches = re.findall(pattern, text, flags=re.M)
    return matches[-1].strip() if matches else ""


def _parse_cert_date(raw):
    """解析 curl 输出的证书日期，如 'Jul  9 02:32:55 2026 GMT' → date"""
    try:
        parts = raw.split()
        if len(parts) < 4:
            return None
        return datetime.strptime(f"{parts[0]} {parts[1]} {parts[3]}", "%b %d %Y").date()
    except ValueError:
        return None


def _extract_cn(distinguished_name):
    """从 'C=CN; ST=Beijing; CN=baidu.com' 中提取 CN 字段"""
    m = re.search(r"CN\s*=\s*([^,;]+)", distinguished_name)
    return m.group(1).strip() if m else ""


def _parse_cert_info(verbose_stderr):
    """从 curl -v 的 stderr 中解析最终连接的 SSL 证书信息"""
    info = {
        "cert_subject": "",
        "cert_issuer": "",
        "cert_cn": "",
        "cert_issuer_cn": "",
        "cert_start_date": "",
        "cert_expire_date": "",
        "cert_days_remaining": None,
        "ssl_verify_ok": False,
    }
    if not verbose_stderr:
        return info

    subject = _last_line_match("subject", verbose_stderr)
    issuer = _last_line_match("issuer", verbose_stderr)
    start_raw = _last_line_match("start date", verbose_stderr)
    expire_raw = _last_line_match("expire date", verbose_stderr)

    info["cert_subject"] = subject
    info["cert_issuer"] = issuer
    info["cert_cn"] = _extract_cn(subject)
    info["cert_issuer_cn"] = _extract_cn(issuer)
    # 兼容不同 TLS 库的输出：'SSL certificate verify ok' / 'verify result: 0 (ok)'
    info["ssl_verify_ok"] = (
        re.search(r"verify\s+(ok\b|result:\s*0)", verbose_stderr) is not None
    )

    start = _parse_cert_date(start_raw)
    expire = _parse_cert_date(expire_raw)
    if start:
        info["cert_start_date"] = start.isoformat()
    if expire:
        info["cert_expire_date"] = expire.isoformat()
        info["cert_days_remaining"] = (expire - datetime.now(timezone.utc).date()).days

    return info


@app.get("/")
async def index(request: Request):
    """首页：服务端渲染"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/test")
async def test_network(request: Request, url: str = Query(..., description="要测试的网址")):
    """测试指定 URL 的网络性能指标与请求详情"""
    try:
        cmd = [
            "curl",
            "-s",                       # 静默模式（不影响 -v）
            "-v",                       # 详细输出，用于解析 SSL 证书信息
            "-L",                       # 跟随重定向
            "-o", "/dev/null",          # 丢弃响应体
            "--max-time", str(CURL_TIMEOUT),
            "-w", CURL_WRITE_OUT,
            url,
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=CURL_TIMEOUT + 5
        )

        if result.returncode != 0:
            return JSONResponse(
                status_code=500,
                content={"error": "网络测试失败，请检查网址是否可达"},
            )

        metrics = result.stdout.strip().split("|")
        if len(metrics) != 15:
            return JSONResponse(
                status_code=500,
                content={"error": "无效的 curl 输出"},
            )

        # 耗时指标（秒 → 毫秒）
        dns = _to_float(metrics[0])
        connect = _to_float(metrics[1])
        appconnect = _to_float(metrics[2])
        pretransfer = _to_float(metrics[3])
        starttransfer = _to_float(metrics[4])
        total = _to_float(metrics[5])

        response = {
            # —— 耗时指标（ms）——
            "dns_time": dns * 1000,                                        # DNS 解析时间
            "tcp_time": (connect - dns) * 1000,                            # TCP 连接时间
            "ssl_time": max(appconnect - connect, 0) * 1000,               # SSL 连接时间
            "prepare_time": max(pretransfer - appconnect, 0) * 1000,       # 预备耗时（发送请求前）
            "first_byte_time": max(starttransfer - pretransfer, 0) * 1000, # 首包响应时间
            "transfer_time": max(total - starttransfer, 0) * 1000,         # 传输耗时（下载响应体）
            "redirect_time": _to_float(metrics[11]) * 1000,                # 重定向总耗时
            "total_time": total * 1000,                                    # 整体耗时
            # —— 请求详情 ——
            "http_code": _to_int(metrics[6]),                              # HTTP 状态码
            "http_version": metrics[7].strip(),                            # HTTP 协议版本
            "remote_ip": metrics[8].strip(),                               # 远端 IP
            "remote_port": metrics[9].strip(),                             # 远端端口
            "num_redirects": _to_int(metrics[10]),                         # 重定向次数
            "size_download": _to_int(metrics[12]),                         # 下载字节数
            "speed_download": _to_float(metrics[13]),                      # 下载速度（B/s）
            "content_type": metrics[14].strip(),                           # 内容类型
        }

        # SSL 证书信息（HTTP 站点为空）
        response.update(_parse_cert_info(result.stderr))
        return response
    except subprocess.TimeoutExpired:
        return JSONResponse(status_code=500, content={"error": "测试超时，请稍后重试"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    import os

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
