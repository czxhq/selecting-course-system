const weekMap = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

const timeFormatTransfer = (times: string[]) => {
  const ctimes: string[] = []
  for (const time of times) {
    const [week, sessionRange, weekRange] = time.split(' ')
    const [startSession, endSession] = sessionRange.split('-').map(Number)
    const [startWeek, endWeek] = weekRange.split('-').map(Number)
    ctimes.push(
      '第' +
        startWeek +
        '-' +
        endWeek +
        '周 ' +
        weekMap[Number(week) - 1] +
        '第' +
        startSession +
        '-' +
        endSession +
        '节'
    )
  }
  return '[' + ctimes.join(',') + ']'
}

const timeToObj = (time: string) => {
  const [week, sessionRange, weekRange] = time.split(' ')
  const [startSession, endSession] = sessionRange.split('-').map(Number)
  const [startWeek, endWeek] = weekRange.split('-').map(Number)
  return {
    weekDay: Number(week),
    startPeriod: startSession,
    endPeriod: endSession,
    startWeek,
    endWeek
  }
}

export const timesToObj = (times: string[]) => {
  const objs = []
  for (const time of times) {
    objs.push(timeToObj(time))
  }
  return objs
}
export default timeFormatTransfer
