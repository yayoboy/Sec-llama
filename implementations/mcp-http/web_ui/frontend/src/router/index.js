import { createRouter, createWebHistory } from 'vue-router'
import DashboardLayout from '@/components/DashboardLayout.vue'
import DashboardView from '@/views/DashboardView.vue'
import ToolsView from '@/views/ToolsView.vue'
import ConfigView from '@/views/ConfigView.vue'
import ApiKeysView from '@/views/ApiKeysView.vue'
import AuditLogsView from '@/views/AuditLogsView.vue'
import AIConfigView from '@/views/AIConfigView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: DashboardLayout,
      children: [
        {
          path: '',
          name: 'dashboard',
          component: DashboardView,
          meta: { title: 'Dashboard' }
        },
        {
          path: 'tools',
          name: 'tools',
          component: ToolsView,
          meta: { title: 'Tools' }
        },
        {
          path: 'config',
          name: 'config',
          component: ConfigView,
          meta: { title: 'Configuration' }
        },
        {
          path: 'api-keys',
          name: 'api-keys',
          component: ApiKeysView,
          meta: { title: 'API Keys' }
        },
        {
          path: 'audit-logs',
          name: 'audit-logs',
          component: AuditLogsView,
          meta: { title: 'Audit Logs' }
        },
        {
          path: 'ai-config',
          name: 'ai-config',
          component: AIConfigView,
          meta: { title: 'AI Configuration' }
        }
      ]
    }
  ]
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} - Sec-Llama` : 'Sec-Llama Web UI'
  next()
})

export default router
