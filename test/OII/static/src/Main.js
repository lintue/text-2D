/**
 * pixel-tree text-2D test, 2020.
 */

import '../styles.scss'

import { Vis } from './Vis'

/* Metadata */

let env = process.env.NODE_ENV

if (env === 'development') { console.log('Development mode.') }

/* Load data */

const data = require('../media/data.json')

const math = document.createElement('script')
math.type = 'text/javascript'
math.id = 'MathJax-script'
math.async = true
math.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'
document.head.appendChild(math)

const $ = require('jquery')

/* Main frames */

const playground = document.createElement('div')
playground.id = 'playground'
document.body.appendChild(playground)

const scrollbox = document.createElement('div')
scrollbox.id = 'scrollbox'
playground.appendChild(scrollbox)

const title = document.createElement('h1')
title.id = 'title'
title.innerText = data.title[0]
playground.appendChild(title)

const subtitle = document.createElement('div')
subtitle.id = 'subtitle'
subtitle.innerText = data.title[1]
title.appendChild(subtitle)

// Toggle subtitle opacity on scroll.
$(document).ready(function() {
  $('#content').scroll(function() {
    if ($('#content').scrollTop() > 0) {
      $('#subtitle').fadeOut()
    } else {
      $('#subtitle').show()
    }
  })
})

const footer = document.createElement('a')
footer.setAttribute('href', 'https://github.com/pixel-tree/licenses/blob/main/MIT-2020')
footer.setAttribute('target', '_blank')
footer.setAttribute('rel', 'noopener')
footer.id = 'footer'
footer.innerText = data.footer
playground.appendChild(footer)

/* Content */

const content = document.createElement('div')
content.id = 'content'
scrollbox.appendChild(content)

const visualisation = new Vis(playground)

/* Exports */

export { data }
