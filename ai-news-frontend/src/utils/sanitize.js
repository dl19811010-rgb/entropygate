/**
 * HTML 安全过滤工具 - XSS 防护
 *
 * 用途：防止 XSS 攻击，对 v-html 渲染的内容进行净化
 * 使用方式：
 *   import { sanitizeHTML } from '@/utils/sanitize'
 *   <div v-html="sanitizeHTML(article.content_html)"></div>
 */

// 白名单标签及其允许的属性
const ALLOWED_TAGS = [
  'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
  'p', 'br', 'hr',
  'ul', 'ol', 'li',
  'blockquote', 'pre', 'code',
  'strong', 'em', 'b', 'i', 'u', 's', 'strike',
  'a', 'img',
  'table', 'thead', 'tbody', 'tr', 'th', 'td',
  'div', 'span', 'section', 'article',
  'figure', 'figcaption',
  'sup', 'sub'
]

const ALLOWED_ATTRS = {
  '*': ['class', 'id', 'style'],
  'a': ['href', 'title', 'target', 'rel'],
  'img': ['src', 'alt', 'title', 'width', 'height', 'loading'],
  'td': ['colspan', 'rowspan'],
  'th': ['colspan', 'rowspan']
}

// 危险模式检测
const DANGEROUS_PATTERNS = [
  /javascript\s*:/gi,
  /on\w+\s*=/gi,
  /<script\b[^>]*>[\s\S]*?<\/script>/gi,
  /<iframe\b[^>]*>[\s\S]*?<\/iframe>/gi,
  /<object\b[^>]*>[\s\S]*?<\/object>/gi,
  /<embed\b[^>]*>/gi,
  /expression\s*\(/gi,
  /url\s*\(\s*['"]?\s*javascript:/gi,
  /vbscript\s*:/gi,
  /data:\s*text\/html/gi
]

/**
 * 净化 HTML 字符串，移除潜在危险的标签和属性
 * @param {string} html - 待净化的 HTML
 * @param {boolean} stripAllTags - 是否完全移除所有标签（纯文本模式）
 * @returns {string} 净化后的安全 HTML
 */
export function sanitizeHTML(html, stripAllTags = false) {
  if (!html || typeof html !== 'string') {
    return ''
  }

  // 1. 检测危险模式并移除
  for (const pattern of DANGEROUS_PATTERNS) {
    if (pattern.test(html)) {
      console.warn('[sanitize] 检测到危险内容并移除:', pattern)
      html = html.replace(pattern, '')
    }
  }

  // 2. 如果要求纯文本模式
  if (stripAllTags) {
    return html.replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').trim()
  }

  // 3. 移除不在白名单中的标签（保留内容）
  const tagRegex = /<\/?([a-zA-Z][a-zA-Z0-9]*)[^>]*>?/g

  let result = html.replace(tagRegex, (match, tagName) => {
    const lowerTag = tagName.toLowerCase()

    if (match.startsWith('</')) {
      if (ALLOWED_TAGS.includes(lowerTag)) return match
      return ''
    }

    if (ALLOWED_TAGS.includes(lowerTag)) {
      return cleanAttributes(match, lowerTag)
    }

    return ''
  })

  return result.trim()
}

/**
 * 清理单个标签上的属性
 */
function cleanAttributes(tagStr, tagName) {
  const allowed = ALLOWED_ATTRS[tagName] || ALLOWED_ATTRS['*'] || []
  const attrRegex = /([\w-]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|(\S+))/g
  let cleanedTag = tagStr

  const foundAttrs = []
  let match
  while ((match = attrRegex.exec(tagStr)) !== null) {
    foundAttrs.push({ name: match[1], full: match[0] })
  }

  for (const attr of foundAttrs) {
    if (!allowed.includes(attr.name.toLowerCase())) {
      cleanedTag = cleanedTag.replace(attr.full, '')
    } else {
      if (attr.name.toLowerCase() === 'href') {
        const hrefMatch = attr.full.match(/=\s*["']?([^"'\s>]*)/)
        if (hrefMatch && /^javascript:/i.test(hrefMatch[1])) {
          cleanedTag = cleanedTag.replace(attr.full, 'href="#" rel="noopener noreferrer"')
        }
      }
    }
  }

  return cleanedTag
}

/**
 * 截取文本到指定长度（用于摘要展示）
 */
export function truncateText(text, maxLength = 200) {
  if (!text) return ''
  const plain = sanitizeHTML(text, true)
  if (plain.length <= maxLength) return plain
  return plain.slice(0, maxLength).trim() + '...'
}
