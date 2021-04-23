/**
 * Visualisation.
 */

import { data } from './Main'

class Vis {
  constructor(container) {

    // Content frame.
    const content = document.getElementById('content')

    // Visualisation frame.
    const frame = document.createElement('div')
    frame.id = 'tSNE'
    content.appendChild(frame)

    /*
     * D3 visualisation.
     */

    const d3 = require('d3v4')

    // Dimensions.
    const width = 900,
          height = 600

    // Legend.
    const legend = d3.select('#content')
      .append('div')
      .attr('id', 'legend')

    // Data graph.
    const svg = d3.select('#tSNE')
      .append('svg')
        .attr('width', '100%')
        .attr('height', '100%')
        .attr('viewBox', [0, 0, width, height])

    // Load data.
    d3.csv('https://raw.githubusercontent.com/pixel-tree/datasets/main/tsne.csv', function(data) {

      // Map for labels/classes.
      let classMap = {
        'Digital Economies': 'one',
        'Digital Knowledge and Culture': 'two',
        'Digital Politics and Government': 'three',
        'Education, Digital Life and Wellbeing': 'four',
        'Ethics and Philosophy of Information': 'five',
        'Information Geography and Inequality': 'six',
        'Information Governance and Security': 'seven'
      }

      // Legend labels.
      let legendLabels = legend.selectAll('text')
      .data(Object.keys(classMap))
      .enter()
      .append('text')
        .attr('class', function(d, i) { return 'legendLabel ' + Object.values(classMap)[i] })
        .text(function(d, i) { return Object.keys(classMap)[i] })
        .on('click', function(d) {
          // If already active, reset graph, else activate other label.
          if (d3.select(this).classed('labelActive')) {
            d3.select(this).classed('labelActive', false)
            d3.selectAll('circle').style('fill', '#c9d5ff')
            d3.selectAll('circle').style('opacity', '1')
          } else {
            // Reset all labels.
            d3.selectAll('text').classed('labelActive', false)
            // Activate chosen label.
            d3.select(this).classed('labelActive', true)
            // Shade inactive data points and leave active points white.
            d3.selectAll('circle').style('fill', '#697ab3')
            d3.selectAll('circle').style('opacity', '0.3')
            d3.select('#tSNE').selectAll('.'+classMap[d]).style('fill', '#c9d5ff')
            d3.select('#tSNE').selectAll('.'+classMap[d]).style('opacity', '1')
          }
        })

      // Graph labels.
      let label = d3.select('#tSNE')
        .append('div')
          .attr('id', 'label')

      // Scale x-axis data.
      let x = d3.scaleLinear()
        .domain([-30, 27])
        .range([0, width])

      // Scale y-axis data.
      let y = d3.scaleLinear()
      .domain([-33, 30])
      .range([height, 0])

      // Replace numerical classes in data with text labels.
      // TO DO: find nicer way to map.
      let classes = function(d) {
        return d.labels.replace(/;/g, '')
                       .replace('1', 'one')
                       .replace('2', 'two')
                       .replace('3', 'three')
                       .replace('4', 'four')
                       .replace('5', 'five')
                       .replace('6', 'six')
                       .replace('7', 'seven')
      }

      // Add dots.
      svg.append('g')
        .selectAll('dot')
        .data(data)
        .enter()
        .append('circle')
          .attr('cx', function (d) { return x(d.x) } )
          .attr('cy', function (d) { return y(d.y) } )
          .attr('class', classes)
          .attr('r', 2.1)
          .style('fill', '#c9d5ff')
          .on('mouseover', function() {
            // Hover mouse over data for details.
            label.style('opacity', 0.95)
          })
          .on('mousemove', function(d) {
            // Map data points with metadata.
            label.html('<p id="labelTitle">' + d.titles + '</p>' +
                       '<p id="labelAuthors">' + d.authors + ' (' + d.years + ')</p>' +
                       '<p id="labelMeta">' + d.labels
                         .replace(/; /g, ';<br>')
                         .replace('1', 'Digital Economies')
                         .replace('2', 'Digital Knowledge and Culture')
                         .replace('3', 'Digital Politics and Government')
                         .replace('4', 'Education, Digital Life and Wellbeing')
                         .replace('5', 'Ethics and Philosophy of Information')
                         .replace('6', 'Information Geography and Inequality')
                         .replace('7', 'Information Governance and Security')
                       + '</p>')
                         .style('left', (d3.event.pageX + 30) + 'px')
                         .style('top', (d3.event.pageY) + 'px')
          })
          .on('mouseleave', function() {
            // Hide.
            label.style('opacity', 0)
          })

    })

    // Generate text.
    for (let i = 0; i < data.vis.length; i++) {

      // Sections.
      let section = document.createElement('div')
      section.classList.add(data.vis[i].id)
      content.appendChild(section)

      // Individual paragraphs.
      for (let j = 0; j < data.vis[i].body.length; j++) {
          let paragraph = document.createElement('p')
          paragraph.innerHTML = data.vis[i].body[j]
          section.appendChild(paragraph)
      }

      // Replace markers {index} with visual media.
      if (typeof data.vis[i].media !== "undefined"
      && data.vis[i].media.length > 0) {
        for (let j = 0; j < data.vis[i].media.length; j++) {
          let path = Object.values(data.vis[i].media[j])
          let alt = Object.keys(data.vis[i].media[j])
          let replacement = section.innerHTML.replace(
            '{' + (j + 1) + '}',
            '<img class="image" src="' + path + '" alt="' + alt + '">'
          )
          section.innerHTML = replacement
        }
      }

      // Replace markers [index] with links.
      if (typeof data.vis[i].links !== "undefined"
      && data.vis[i].links.length > 0) {
        for (let j = 0; j < data.vis[i].links.length; j++) {
          let url = Object.values(data.vis[i].links[j])
          let intext = Object.keys(data.vis[i].links[j])
          let replacement = section.innerHTML.replace(
            '[' + (j + 1) + ']',
            '<a target="_blank" rel="noopener" href="' + url + '">' + intext + '</a>'
          )
          section.innerHTML = replacement
        }
      }

    }

  }
}

export { Vis }
