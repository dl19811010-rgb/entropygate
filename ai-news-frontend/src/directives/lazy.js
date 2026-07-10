/**
 * v-lazy 图片懒加载指令
 *
 * 使用方式：
 *   <img v-lazy="imageUrl" alt="..." />
 *   <div v-lazy:background="bgUrl"></div>
 *
 * 原理：使用 IntersectionObserver，当元素进入视口时才加载图片
 */

const lazyCache = new Map()

function createObserver() {
  return new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target
        const { src, isBg } = lazyCache.get(el)

        if (isBg) {
          el.style.backgroundImage = `url(${src})`
        } else {
          el.src = src
        }

        el.classList.add('lazy-loaded')
        lazyCache.delete(el)
        observer.unobserve(el)
      }
    })
  }, {
    rootMargin: '100px',
    threshold: 0.1
  })
}

let observer = null

function getObserver() {
  if (!observer) observer = createObserver()
  return observer
}

export default {
  mounted(el, binding) {
    const src = binding.value
    if (!src) return

    const placeholder = 'data:image/svg+xml,' + encodeURIComponent(
      '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="9" fill="%23f1f5f9"><rect width="100%" height="100%"/></svg>'
    )

    const isBg = binding.arg === 'background'

    if (isBg) {
      el.style.backgroundImage = `url(${placeholder})`
      el.style.backgroundSize = 'cover'
      el.style.backgroundPosition = 'center'
      el.classList.add('lazy-bg')
    } else {
      el.src = placeholder
      el.classList.add('lazy-img')
    }

    lazyCache.set(el, { src, isBg })
    getObserver().observe(el)
  },

  unmounted(el) {
    lazyCache.delete(el)
    if (observer) observer.unobserve(el)
  }
}
