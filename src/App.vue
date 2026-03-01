<template>
  <div class="app">
    <header class="header">
      <h1>网络性能测试工具</h1>
    </header>
    <main class="main">
      <div class="test-form">
        <div class="form-group">
          <label for="url">测试 URL:</label>
          <input 
            type="url" 
            id="url" 
            v-model="testUrl" 
            placeholder="请输入要测试的网址，例如：https://www.example.com"
            required
          />
        </div>
        <button 
          class="test-btn" 
          @click="startTest"
          :disabled="isTesting"
        >
          {{ isTesting ? '测试中...' : '开始测试' }}
        </button>
      </div>
      
      <div v-if="testResults" class="test-results">
        <h2>测试结果</h2>
        <div class="results-grid">
          <div class="result-item">
            <div class="result-label">DNS 请求时间</div>
            <div class="result-value">{{ testResults.dns_time.toFixed(2) }} ms</div>
          </div>
          <div class="result-item">
            <div class="result-label">TCP 建连时间</div>
            <div class="result-value">{{ testResults.tcp_time.toFixed(2) }} ms</div>
          </div>
          <div class="result-item">
            <div class="result-label">SSL 建连时间</div>
            <div class="result-value">{{ testResults.ssl_time.toFixed(2) }} ms</div>
          </div>
          <div class="result-item">
            <div class="result-label">首包响应时间</div>
            <div class="result-value">{{ testResults.first_byte_time.toFixed(2) }} ms</div>
          </div>
          <div class="result-item full-width">
            <div class="result-label">整体耗时</div>
            <div class="result-value total">{{ testResults.total_time.toFixed(2) }} ms</div>
          </div>
        </div>
      </div>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </main>
    <footer class="footer">
      <p>网络性能测试工具 © 2026</p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const testUrl = ref('https://www.baidu.com')
const isTesting = ref(false)
const testResults = ref(null)
const error = ref('')

const startTest = async () => {
  if (!testUrl.value) {
    error.value = '请输入测试 URL'
    return
  }
  
  isTesting.value = true
  error.value = ''
  testResults.value = null
  
  try {
    const response = await fetch(`/api/test?url=${encodeURIComponent(testUrl.value)}`)
    if (!response.ok) {
      throw new Error('测试失败，请检查网络连接')
    }
    const data = await response.json()
    testResults.value = data
  } catch (err) {
    error.value = err.message
  } finally {
    isTesting.value = false
  }
}
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
}

.header {
  background-color: #3498db;
  color: white;
  padding: 2rem 0;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: 600;
}

.main {
  flex: 1;
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
}

.test-form {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.1);
}

.test-btn {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.test-btn:hover:not(:disabled) {
  background-color: #2980b9;
}

.test-btn:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.test-results {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-top: 2rem;
}

.test-results h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #333;
  font-size: 1.5rem;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.result-item {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  border-left: 4px solid #3498db;
}

.result-item.full-width {
  grid-column: 1 / -1;
}

.result-label {
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.result-value {
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
}

.result-value.total {
  color: #e74c3c;
  font-size: 1.5rem;
}

.error-message {
  background-color: #fee;
  color: #c00;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
  border-left: 4px solid #e74c3c;
}

.footer {
  background-color: #333;
  color: white;
  padding: 1rem 0;
  text-align: center;
  margin-top: 2rem;
}

.footer p {
  margin: 0;
  font-size: 0.875rem;
  color: #bdc3c7;
}

@media (max-width: 768px) {
  .main {
    padding: 1rem;
  }
  
  .test-form,
  .test-results {
    padding: 1.5rem;
  }
  
  .results-grid {
    grid-template-columns: 1fr;
  }
}
</style>