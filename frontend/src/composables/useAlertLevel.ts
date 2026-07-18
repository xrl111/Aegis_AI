import { computed } from 'vue'
import { ALERT_CONFIG } from '@/utils/constants'
import type { AlertLevel } from '@/types'

export function useAlertLevel(level: () => AlertLevel) {
  const config = computed(() => ALERT_CONFIG[level()])
  const color = computed(() => config.value.color)
  const bg = computed(() => config.value.bg)
  const label = computed(() => config.value.label)
  const icon = computed(() => config.value.icon)

  const borderClass = computed(() => {
    const c = config.value.color
    return `border-l-[3px]`
  })

  const badgeClass = computed(() => {
    const c = config.value.color
    return `inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium`
  })

  return { config, color, bg, label, icon, borderClass, badgeClass }
}
