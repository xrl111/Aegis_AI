import { ref, watch } from 'vue'

export function useDebounce<T>(value: () => T, delay = 300) {
  const debounced = ref(value()) as { value: T }

  let timer: ReturnType<typeof setTimeout>
  watch(value, (v) => {
    clearTimeout(timer)
    timer = setTimeout(() => {
      debounced.value = v
    }, delay)
  })

  return debounced
}
