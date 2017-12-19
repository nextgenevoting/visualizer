<template>
  <div class="scratch-card">
    <canvas v-if="!this.revealed" width="100" height="100" :style="scratchable ? 'cursor: url(/public/coin.ico), auto' : 'cursor: not-allowed'"></canvas>
    <div>
      <slot></slot>
    </div>
  </div>
</template>

<script scoped>
export default {
  data: () => ({
  }),
  props: {
    scratchable: {
      type: Boolean,
      required: false,
      default: true
    },
    revealed: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  mounted () {
    if (!this.revealed) {
      scratchCard(this.$el, this.scratchable, () => {
        // this.revealed = true
        this.$emit('revealed')
      })
    }
  }
}

function scratchCard (container, scratchable, reveal) {
  var isDrawing, lastPoint
  var canvas = container.querySelector('canvas')
  var ctx = canvas.getContext('2d')
  var brush = new Image()
  var dim = canvas.parentNode.getBoundingClientRect()

  brush.src = '/public/brush.png' // TODO

  canvas.width = dim.width
  canvas.height = dim.height
  ctx.fillStyle = '#c0c0c0'
  ctx.fillRect(0, 0, canvas.width, canvas.height)

  if (scratchable) {
    canvas.addEventListener('mousedown', handleMouseDown, false)
    canvas.addEventListener('touchstart', handleMouseDown, false)
    canvas.addEventListener('mousemove', handleMouseMove, false)
    canvas.addEventListener('touchmove', handleMouseMove, false)
    canvas.addEventListener('mouseup', handleMouseUp, false)
    canvas.addEventListener('touchend', handleMouseUp, false)
  }

  function distanceBetween (point1, point2) {
    return Math.sqrt(Math.pow(point2.x - point1.x, 2) + Math.pow(point2.y - point1.y, 2))
  }

  function angleBetween (point1, point2) {
    return Math.atan2(point2.x - point1.x, point2.y - point1.y)
  }

  // Only test every `stride` pixel. `stride`x faster,
  // but might lead to inaccuracy
  function getFilledInPixels (stride) {
    if (!stride || stride < 1) {
      stride = 1
    }

    var pixels = ctx.getImageData(0, 0, canvas.width, canvas.height)
    var pdata = pixels.data
    var l = pdata.length
    var total = (l / stride)
    var count = 0

    // Iterate over all pixels
    for (var i = count = 0; i < l; i += stride) {
      if (parseInt(pdata[i]) === 0) {
        count++
      }
    }

    return Math.round((count / total) * 100)
  }

  function getMouse (e, canvas) {
    var offsetX = 0
    var offsetY = 0
    var mx, my

    if (canvas.offsetParent !== undefined) {
      do {
        offsetX += canvas.offsetLeft
        offsetY += canvas.offsetTop
      } while ((canvas = canvas.offsetParent))
    }

    mx = (e.pageX || e.touches[0].clientX) - offsetX
    my = (e.pageY || e.touches[0].clientY) - offsetY

    return { x: mx, y: my }
  }

  function handlePercentage (filledInPixels) {
    filledInPixels = filledInPixels || 0
    if (filledInPixels > 80) {
      canvas.parentNode.removeChild(canvas)
      reveal()
    }
  }

  function handleMouseDown (e) {
    isDrawing = true
    lastPoint = getMouse(e, canvas)
  }

  function handleMouseMove (e) {
    if (!isDrawing) {
      return
    }

    e.preventDefault()

    var currentPoint = getMouse(e, canvas)
    var dist = distanceBetween(lastPoint, currentPoint)
    var angle = angleBetween(lastPoint, currentPoint)
    var x, y

    for (var i = 0; i < dist; i++) {
      x = lastPoint.x + (Math.sin(angle) * i) - 25
      y = lastPoint.y + (Math.cos(angle) * i) - 25
      ctx.globalCompositeOperation = 'destination-out'
      ctx.drawImage(brush, x, y)
    }

    lastPoint = currentPoint
    handlePercentage(getFilledInPixels(32))
  }

  function handleMouseUp (e) {
    isDrawing = false
  }
}
</script>

<style scoped>
.scratch-card {
  position: relative;
  user-select: none;
}
canvas {
  position: absolute;
  top: 0;
  border-radius: 10px;
}
</style>
