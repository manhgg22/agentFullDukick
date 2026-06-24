<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NSelect, NTooltip } from 'naive-ui'
import { setServerUrl, setApiKey } from '@/api/client'

const AGENTS = [
  { label: '🎯 Tổng Coordinator', value: 'http://localhost:9001', token: '' },
  { label: '📣 Sales Agent',       value: 'http://localhost:9002', token: '' },
  { label: '📋 Account Agent',     value: 'http://localhost:9003', token: '' },
  { label: '🎨 Creative Agent',    value: 'http://localhost:9004', token: '' },
  { label: '💰 Finance Agent',     value: 'http://localhost:9005', token: '' },
]

const current = ref(localStorage.getItem('hermes_server_url') || 'http://localhost:9001')

onMounted(() => {
  if (!localStorage.getItem('hermes_server_url')) {
    setServerUrl('http://localhost:9001')
  }
})

function switchAgent(url: string) {
  if (url === current.value) return
  current.value = url
  setServerUrl(url)
  // Clear auth token — each agent has its own token
  setApiKey('')
  localStorage.removeItem('hermes_api_key')
  localStorage.removeItem('hermes_user_role')
  // Redirect to login
  window.location.href = '/#/login'
  window.location.reload()
}
</script>

<template>
  <div class="agent-switcher">
    <NTooltip placement="right">
      <template #trigger>
        <NSelect
          :value="current"
          :options="AGENTS"
          size="small"
          style="width: 100%"
          @update:value="switchAgent"
        />
      </template>
      Chọn agent Dukick
    </NTooltip>
  </div>
</template>

<style scoped>
.agent-switcher {
  padding: 8px 12px;
  border-bottom: 1px solid var(--n-border-color, #2a2a2a);
  margin-bottom: 4px;
}
</style>
