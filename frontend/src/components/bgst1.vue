<template>
  <canvas ref="canvas"></canvas>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { TweenLite, Circ } from 'gsap' // 确保 gsap 已安装

const canvas = ref(null)

let width,
  height,
  ctx,
  points,
  target,
  animateHeader = true

function initHeader() {
  width = window.innerWidth
  height = window.innerHeight
  target = { x: width / 2, y: height / 2 }

  // 设置 canvas 尺寸和上下文
  const canvasElement = canvas.value
  canvasElement.width = width
  canvasElement.height = height
  ctx = canvasElement.getContext('2d')

  // 创建点
  points = []
  for (let x = 0; x < width; x += width / 20) {
    for (let y = 0; y < height; y += height / 20) {
      const px = x + (Math.random() * width) / 20
      const py = y + (Math.random() * height) / 20
      const point = { x: px, originX: px, y: py, originY: py }
      points.push(point)
    }
  }

  // 为每个点找到最近的 5 个点
  points.forEach((p1) => {
    const closest = []
    points.forEach((p2) => {
      if (p1 !== p2) {
        let placed = false
        for (let k = 0; k < 5; k++) {
          if (!placed) {
            if (!closest[k]) {
              closest[k] = p2
              placed = true
            }
          }
        }
        for (let k = 0; k < 5; k++) {
          if (!placed) {
            if (getDistance(p1, p2) < getDistance(p1, closest[k])) {
              closest[k] = p2
              placed = true
            }
          }
        }
      }
    })
    p1.closest = closest
  })

  // 为每个点分配一个圆
  points.forEach((point) => {
    const circle = new Circle(
      point,
      2 + Math.random() * 2,
      'rgba(255,255,255,0.3)'
    )
    point.circle = circle
  })
}

function addListeners() {
  if (!('ontouchstart' in window)) {
    window.addEventListener('mousemove', mouseMove)
  }
  window.addEventListener('scroll', scrollCheck)
  window.addEventListener('resize', resize)
}

function removeListeners() {
  if (!('ontouchstart' in window)) {
    window.removeEventListener('mousemove', mouseMove)
  }
  window.removeEventListener('scroll', scrollCheck)
  window.removeEventListener('resize', resize)
}

function mouseMove(e) {
  const posx =
    e.pageX ||
    e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft
  const posy =
    e.pageY ||
    e.clientY + document.body.scrollTop + document.documentElement.scrollTop
  target.x = posx
  target.y = posy
}

function scrollCheck() {
  animateHeader = document.body.scrollTop <= height
}

function resize() {
  width = window.innerWidth
  height = window.innerHeight
  const canvasElement = canvas.value
  canvasElement.width = width
  canvasElement.height = height
}

function initAnimation() {
  animate()
  points.forEach((point) => shiftPoint(point))
}

function animate() {
  if (animateHeader) {
    ctx.clearRect(0, 0, width, height)
    points.forEach((point) => {
      // 检测点的范围
      const distance = Math.abs(getDistance(target, point))
      if (distance < 4000) {
        point.active = 0.3
        point.circle.active = 0.6
      } else if (distance < 20000) {
        point.active = 0.1
        point.circle.active = 0.3
      } else if (distance < 40000) {
        point.active = 0.02
        point.circle.active = 0.1
      } else {
        point.active = 0
        point.circle.active = 0
      }

      drawLines(point)
      point.circle.draw()
    })
  }
  requestAnimationFrame(animate)
}

function shiftPoint(p) {
  TweenLite.to(p, 1 + Math.random(), {
    x: p.originX - 50 + Math.random() * 100,
    y: p.originY - 50 + Math.random() * 100,
    ease: Circ.easeInOut,
    onComplete: () => shiftPoint(p)
  })
}

function drawLines(p) {
  if (!p.active) return
  p.closest.forEach((closestPoint) => {
    ctx.beginPath()
    ctx.moveTo(p.x, p.y)
    ctx.lineTo(closestPoint.x, closestPoint.y)
    ctx.strokeStyle = `rgba(156,217,249,${p.active})`
    ctx.stroke()
  })
}

function Circle(pos, rad, color) {
  this.pos = pos || null
  this.radius = rad || null
  this.color = color || null

  this.draw = function () {
    if (!this.active) return
    ctx.beginPath()
    ctx.arc(this.pos.x, this.pos.y, this.radius, 0, 2 * Math.PI, false)
    ctx.fillStyle = `rgba(156,217,249,${this.active})`
    ctx.fill()
  }
}

function getDistance(p1, p2) {
  return Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2)
}

onMounted(() => {
  initHeader()
  initAnimation()
  addListeners()
})

onBeforeUnmount(() => {
  removeListeners()
})
</script>
