/* 网络性能测试工具 - 前端逻辑（原生 JS，无框架） */

(function () {
  "use strict";

  var form = document.getElementById("test-form");
  var urlInput = document.getElementById("url-input");
  var submitBtn = document.getElementById("submit-btn");
  var errorMsg = document.getElementById("error-msg");
  var resultPanel = document.getElementById("result-panel");
  var detailPanel = document.getElementById("detail-panel");
  var sslPanel = document.getElementById("ssl-panel");
  var resultUrl = document.getElementById("result-url");

  var TIME_FIELDS = [
    "dns_time",
    "tcp_time",
    "ssl_time",
    "prepare_time",
    "first_byte_time",
    "transfer_time",
    "redirect_time",
    "total_time",
  ];

  function fmt(value) {
    return value.toFixed(2);
  }

  function fmtBytes(bytes) {
    if (!bytes || bytes <= 0) return "-";
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + " KB";
    return (bytes / 1024 / 1024).toFixed(2) + " MB";
  }

  function fmtSpeed(bytesPerSec) {
    if (!bytesPerSec || bytesPerSec <= 0) return "-";
    if (bytesPerSec < 1024) return bytesPerSec.toFixed(0) + " B/s";
    if (bytesPerSec < 1024 * 1024) return (bytesPerSec / 1024).toFixed(2) + " KB/s";
    return (bytesPerSec / 1024 / 1024).toFixed(2) + " MB/s";
  }

  function setText(id, text) {
    var el = document.getElementById(id);
    if (el) el.textContent = text;
  }

  function render(data) {
    var total = data.total_time || 0;

    // 耗时指标表
    TIME_FIELDS.forEach(function (key) {
      setText(key, fmt(data[key]));
      var ratioCell = document.getElementById(key + "_ratio");
      if (ratioCell) {
        ratioCell.textContent =
          key === "total_time" || total <= 0
            ? "-"
            : ((data[key] / total) * 100).toFixed(1) + "%";
      }
    });

    // 请求详情表
    var code = data.http_code;
    var codeEl = document.getElementById("http_code");
    if (codeEl) {
      codeEl.textContent = code || "-";
      codeEl.className = "num " + (code >= 200 && code < 400 ? "code-ok" : "code-bad");
    }

    setText("http_version", data.http_version ? "HTTP/" + data.http_version : "-");
    setText("server_info", data.server || "-");

    var addr =
      data.remote_ip && data.remote_port
        ? data.remote_ip + ":" + data.remote_port
        : data.remote_ip || "-";
    setText("remote_addr", addr);

    setText("num_redirects", data.num_redirects);
    setText("size_download", fmtBytes(data.size_download));
    setText("speed_download", fmtSpeed(data.speed_download));
    setText("content_type", data.content_type || "-");

    // SSL 证书信息（HTTP 站点为空）
    setText("ssl_protocol", data.ssl_protocol || "-");
    setText("ssl_cipher", data.ssl_cipher || "-");
    setText("cert_cn", data.cert_cn || "-");
    setText("cert_issuer_cn", data.cert_issuer_cn || "-");

    var validityEl = document.getElementById("cert_validity");
    if (validityEl) {
      validityEl.textContent =
        data.cert_start_date && data.cert_expire_date
          ? data.cert_start_date + " ~ " + data.cert_expire_date
          : "-";
    }

    var daysEl = document.getElementById("cert_days");
    if (daysEl) {
      if (data.cert_days_remaining !== null && data.cert_days_remaining !== undefined) {
        var days = data.cert_days_remaining;
        daysEl.textContent = days + " 天";
        daysEl.className = "num " + (days < 30 ? "code-bad" : "");
      } else {
        daysEl.textContent = "-";
        daysEl.className = "num";
      }
    }

    var verifyEl = document.getElementById("ssl_verify");
    if (verifyEl) {
      if (data.cert_cn) {
        verifyEl.textContent = data.ssl_verify_ok ? "通过" : "未通过";
        verifyEl.className = "num " + (data.ssl_verify_ok ? "code-ok" : "code-bad");
      } else {
        verifyEl.textContent = "-";
        verifyEl.className = "num";
      }
    }

    resultUrl.textContent = urlInput.value.trim();
    resultPanel.hidden = false;
    detailPanel.hidden = false;
    // HTTP 站点无 SSL 信息，隐藏面板
    sslPanel.hidden = !(data.cert_cn || data.ssl_protocol);
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    var url = urlInput.value.trim();
    if (!url) return;

    if (!/^https?:\/\//i.test(url)) {
      url = "https://" + url;
      urlInput.value = url;
    }

    errorMsg.hidden = true;
    submitBtn.disabled = true;
    submitBtn.textContent = "测试中...";

    fetch("/api/test?url=" + encodeURIComponent(url))
      .then(function (res) {
        return res.json().then(function (data) {
          return { ok: res.ok, data: data };
        });
      })
      .then(function (result) {
        if (!result.ok || result.data.error) {
          throw new Error(result.data.error || "网络请求失败，请稍后重试");
        }
        render(result.data);
      })
      .catch(function (err) {
        errorMsg.textContent = err.message || "请求失败，请稍后重试";
        errorMsg.hidden = false;
      })
      .finally(function () {
        submitBtn.disabled = false;
        submitBtn.textContent = "开始测试";
      });
  });
})();
