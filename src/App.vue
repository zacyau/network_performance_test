<template>
  <div class="app">
    <div class="background">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
    </div>

    <header class="header">
      <div class="logo">
        <svg class="logo-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
        </svg>
        <span class="logo-text">NetSpeed</span>
      </div>
      <p class="tagline">专业的网络性能测试工具</p>
    </header>

    <main class="main">
      <div class="test-card" :class="{ 'testing': isTesting }">
        <div class="card-header">
          <h2>开始测试</h2>
          <p>输入网址，即刻了解网络性能</p>
        </div>

        <div class="input-wrapper">
          <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="2" y1="12" x2="22" y2="12"/>
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
          </svg>
          <input
            type="url"
            v-model="testUrl"
            placeholder="输入要测试的网址"
            @keyup.enter="startTest"
            :disabled="isTesting"
          />
          <button class="clear-btn" v-if="testUrl && !isTesting" @click="testUrl = ''">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <button class="test-btn" @click="startTest" :disabled="isTesting">
          <span v-if="!isTesting" class="btn-content">
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="5 3 19 12 5 21 5 3"/>
            </svg>
            开始测试
          </span>
          <span v-else class="btn-content loading">
            <div class="spinner"></div>
            测试中...
          </span>
        </button>
      </div>

      <transition name="fade-slide">
        <div v-if="testResults" class="results-card">
          <div class="results-header">
            <h3>测试结果</h3>
            <span class="url-badge">{{ testUrl }}</span>
          </div>

          <div class="metrics-row">
            <div class="metrics-row-inner">
              <div class="metric-item" style="--delay: 0">
                <div class="metric-icon dns">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
                    <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
                    <line x1="12" y1="22.08" x2="12" y2="12"/>
                  </svg>
                </div>
                <div class="metric-info">
                  <span class="metric-label">DNS 解析</span>
                  <span class="metric-value">{{ testResults.dns_time.toFixed(2) }} <small>ms</small></span>
                </div>
                <div class="metric-bar">
                  <div class="metric-progress" :style="{ width: getBarWidth(testResults.dns_time) + '%' }"></div>
                </div>
              </div>

              <div class="metric-item" style="--delay: 1">
                <div class="metric-icon tcp">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                    <line x1="3" y1="9" x2="21" y2="9"/>
                    <line x1="9" y1="21" x2="9" y2="9"/>
                  </svg>
                </div>
                <div class="metric-info">
                  <span class="metric-label">TCP 连接</span>
                  <span class="metric-value">{{ testResults.tcp_time.toFixed(2) }} <small>ms</small></span>
                </div>
                <div class="metric-bar">
                  <div class="metric-progress tcp" :style="{ width: getBarWidth(testResults.tcp_time) + '%' }"></div>
                </div>
              </div>
            </div>

            <div class="metrics-row-inner">
              <div class="metric-item" style="--delay: 2">
                <div class="metric-icon ssl">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                  </svg>
                </div>
                <div class="metric-info">
                  <span class="metric-label">SSL 握手</span>
                  <span class="metric-value">{{ testResults.ssl_time.toFixed(2) }} <small>ms</small></span>
                </div>
                <div class="metric-bar">
                  <div class="metric-progress ssl" :style="{ width: getBarWidth(testResults.ssl_time) + '%' }"></div>
                </div>
              </div>

              <div class="metric-item" style="--delay: 3">
                <div class="metric-icon ttfb">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
                  </svg>
                </div>
                <div class="metric-info">
                  <span class="metric-label">首包响应</span>
                  <span class="metric-value">{{ testResults.first_byte_time.toFixed(2) }} <small>ms</small></span>
                </div>
                <div class="metric-bar">
                  <div class="metric-progress ttfb" :style="{ width: getBarWidth(testResults.first_byte_time) + '%' }"></div>
                </div>
              </div>
            </div>
          </div>

          <div class="total-metric">
            <div class="total-info">
              <svg class="total-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
              <div>
                <span class="total-label">整体耗时</span>
                <span class="total-value">{{ testResults.total_time.toFixed(2) }} ms</span>
              </div>
            </div>
            <div class="total-grade" :class="getGrade(testResults.total_time)">
              {{ getGradeText(testResults.total_time) }}
            </div>
          </div>
        </div>
      </transition>

      <transition name="fade-slide">
        <div v-if="error" class="error-toast">
          <svg class="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          <span>{{ error }}</span>
          <button class="error-close" @click="error = ''">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
      </transition>
    </main>

    <footer class="footer">
      <p>Made with <span class="heart">♥</span> for developers</p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const testUrl = ref('https://www.baidu.com')
const isTesting = ref(false)
const testResults = ref(null)
const error = ref('')

const getBarWidth = (value) => {
  return Math.min((value / 500) * 100, 100)
}

const getGrade = (time) => {
  if (time < 100) return 'excellent'
  if (time < 200) return 'good'
  if (time < 500) return 'fair'
  return 'poor'
}

const getGradeText = (time) => {
  if (time < 100) return '极速'
  if (time < 200) return '优秀'
  if (time < 500) return '一般'
  return '较慢'
}

const startTest = async () => {
  if (!testUrl.value) {
    error.value = '请输入要测试的网址'
    setTimeout(() => error.value = '', 3000)
    return
  }

  if (!testUrl.value.startsWith('http://') && !testUrl.value.startsWith('https://')) {
    testUrl.value = 'https://' + testUrl.value
  }

  isTesting.value = true
  error.value = ''
  testResults.value = null

  try {
    const response = await fetch(`/api/test?url=${encodeURIComponent(testUrl.value)}`)
    if (!response.ok) {
      throw new Error('网络请求失败，请稍后重试')
    }
    const data = await response.json()
    testResults.value = data
  } catch (err) {
    error.value = err.message
    setTimeout(() => error.value = '', 5000)
  } finally {
    isTesting.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app {
  min-height: 100vh;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
  color: #ffffff;
  position: relative;
  overflow-x: hidden;
}

.background {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  z-index: 0;
  pointer-events: none;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: #667eea;
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: #764ba2;
  bottom: -50px;
  left: -50px;
  animation-delay: -5s;
}

.orb-3 {
  width: 250px;
  height: 250px;
  background: #f093fb;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -10s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(20px, -30px) scale(1.05); }
  50% { transform: translate(-20px, 20px) scale(0.95); }
  75% { transform: translate(30px, 10px) scale(1.02); }
}

.header {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 3rem 2rem 2rem;
}

.logo {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.logo-icon {
  width: 2.5rem;
  height: 2.5rem;
  color: #667eea;
}

.logo-text {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.tagline {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 400;
}

.main {
  position: relative;
  z-index: 1;
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
}

.test-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 2.5rem;
  margin-bottom: 2rem;
  transition: all 0.3s ease;
}

.test-card.testing {
  border-color: rgba(102, 126, 234, 0.5);
  box-shadow: 0 0 30px rgba(102, 126, 234, 0.2);
}

.card-header {
  margin-bottom: 1.5rem;
}

.card-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.card-header p {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.5);
}

.input-wrapper {
  position: relative;
  margin-bottom: 1rem;
}

.input-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.25rem;
  height: 1.25rem;
  color: rgba(255, 255, 255, 0.4);
  pointer-events: none;
}

.input-wrapper input {
  width: 100%;
  padding: 1rem 3rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  font-size: 1rem;
  color: #fff;
  transition: all 0.3s ease;
}

.input-wrapper input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.input-wrapper input:focus {
  outline: none;
  border-color: #667eea;
  background: rgba(255, 255, 255, 0.12);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}

.input-wrapper input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.clear-btn {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.5rem;
  height: 1.5rem;
  padding: 0;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.clear-btn svg {
  width: 0.75rem;
  height: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
}

.clear-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.test-btn {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  color: #fff;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
  position: relative;
}

.test-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

.test-btn:active:not(:disabled) {
  transform: translateY(0);
}

.test-btn:disabled {
  opacity: 0.8;
  cursor: not-allowed;
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.spinner {
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.results-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 2.5rem;
}

.results-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.results-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
}

.url-badge {
  font-size: 0.75rem;
  padding: 0.375rem 0.75rem;
  background: rgba(102, 126, 234, 0.2);
  border-radius: 20px;
  color: rgba(255, 255, 255, 0.8);
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.metrics-row {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.metrics-row-inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.metric-item {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  animation: slideIn 0.4s ease forwards;
  animation-delay: calc(var(--delay) * 0.1s);
  opacity: 0;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.metric-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.metric-icon svg {
  width: 1.5rem;
  height: 1.5rem;
}

.metric-icon.dns {
  background: rgba(102, 126, 234, 0.2);
  color: #667eea;
}

.metric-icon.tcp {
  background: rgba(118, 75, 162, 0.2);
  color: #764ba2;
}

.metric-icon.ssl {
  background: rgba(240, 147, 251, 0.2);
  color: #f093fb;
}

.metric-icon.ttfb {
  background: rgba(255, 107, 107, 0.2);
  color: #ff6b6b;
}

.metric-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  min-width: 0;
}

.metric-label {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.5);
}

.metric-value {
  font-size: 1.5rem;
  font-weight: 700;
}

.metric-value small {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.5);
  font-weight: 400;
}

.metric-bar {
  width: 100px;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
  flex-shrink: 0;
}

.metric-progress {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 4px;
  transition: width 0.6s ease;
}

.metric-progress.tcp {
  background: linear-gradient(90deg, #764ba2, #f093fb);
}

.metric-progress.ssl {
  background: linear-gradient(90deg, #f093fb, #ff6b6b);
}

.metric-progress.ttfb {
  background: linear-gradient(90deg, #ff6b6b, #ffd93d);
}

.total-metric {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
  border: 1px solid rgba(102, 126, 234, 0.3);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.total-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.total-icon {
  width: 2.5rem;
  height: 2.5rem;
  color: #667eea;
}

.total-label {
  display: block;
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 0.25rem;
}

.total-value {
  font-size: 2rem;
  font-weight: 700;
}

.total-grade {
  padding: 0.75rem 1.5rem;
  border-radius: 20px;
  font-size: 1rem;
  font-weight: 600;
}

.total-grade.excellent {
  background: rgba(72, 199, 142, 0.2);
  color: #48c78e;
}

.total-grade.good {
  background: rgba(102, 126, 234, 0.2);
  color: #667eea;
}

.total-grade.fair {
  background: rgba(255, 217, 61, 0.2);
  color: #ffd93d;
}

.total-grade.poor {
  background: rgba(255, 107, 107, 0.2);
  color: #ff6b6b;
}

.error-toast {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(255, 107, 107, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #fff;
  font-size: 0.875rem;
  font-weight: 500;
  box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
  z-index: 100;
}

.error-icon {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
}

.error-close {
  background: none;
  border: none;
  padding: 0.25rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 0.5rem;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.error-close:hover {
  opacity: 1;
}

.error-close svg {
  width: 1rem;
  height: 1rem;
}

.footer {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 2rem;
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.875rem;
}

.heart {
  color: #ff6b6b;
}

.fade-slide-enter-active {
  transition: all 0.4s ease;
}

.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@media (max-width: 640px) {
  .header {
    padding: 2rem 1.5rem 1.5rem;
  }

  .logo-text {
    font-size: 1.5rem;
  }

  .main {
    padding: 1.5rem;
    max-width: 100%;
  }

  .test-card,
  .results-card {
    padding: 1.5rem;
    border-radius: 20px;
  }

  .metrics-row-inner {
    grid-template-columns: 1fr;
  }

  .metric-item {
    padding: 1rem;
  }

  .metric-icon {
    width: 2.5rem;
    height: 2.5rem;
  }

  .metric-icon svg {
    width: 1.25rem;
    height: 1.25rem;
  }

  .metric-value {
    font-size: 1.25rem;
  }

  .metric-bar {
    display: none;
  }

  .total-metric {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .total-info {
    flex-direction: column;
  }

  .total-value {
    font-size: 1.5rem;
  }
}
</style>