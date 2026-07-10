/**
 * 统一的日志工具
 * - 开发环境：保留 console 输出，便于调试
 * - 生产环境：静默处理（后续可接入监控上报，如 Sentry）
 */

const isDev = import.meta.env.DEV

export function logError(context, error) {
  if (isDev) {
    console.error(context, error)
  }
  // TODO: 生产环境可接入错误监控上报
}

export function logWarn(context, ...args) {
  if (isDev) {
    console.warn(context, ...args)
  }
}

export function logInfo(context, ...args) {
  if (isDev) {
    console.log(context, ...args)
  }
}
