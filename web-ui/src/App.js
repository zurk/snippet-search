import React, { Component } from 'react';

import './App.css';

//D3
import { select, selectAll } from 'd3-selection';
import { scaleLinear, scaleOrdinal, schemeCategory20 } from 'd3-scale';
import { max } from 'd3-array';

const splitLines = linesRaw => linesRaw.split('\n');

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      code: [],
      snippets: [],
    };
  }

  handleChange = (evt) => {
    var files = evt.target.files;
    for (let i = 0, filesCount = files.length; i < filesCount; i++) {
      var reader = new FileReader();
      reader.onload = evt => {
        const sourceCode = evt.target.result;
        this.setState({code: splitLines(sourceCode)})

        const payload = {
          method: 'POST',
          cache: 'default',
          body: JSON.stringify({
            content: sourceCode,
          }),
        };

        var myRequest = new Request('http://localhost:8080/parse');

        fetch(myRequest, payload)
          .then(response => response.json())
          .then(data => this.setState({
            snippets: data,
          }));
      };

      reader.readAsText(files[i]);
    }
  }

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <h2>Snippet search</h2>
        </div>

        <form>
          <input type="file" id="files" name="files[]" multiple onChange={e=>this.handleChange(e)} />
        </form>

        <SnippetViewer
          snippets={this.state.snippets}
          lines={this.state.code}
          width={960}
          height={900}
        />

      </div>
    );
  }
}

const COLOR_TRANSPARENT = '#BBB';
const LINE_HEIGHT = 17.32;
const CHAR_WIDTH = 8.4

const padd = (number, length) => {
  const missingLength = length - numberLength(number);
  if (missingLength <= 0) {
    return number;
  }

  const paddParts = [];
  paddParts.length = missingLength + 1;
  return paddParts.join('0') + number;
};

const numberLength = number => number === 0 ? 1 : Math.ceil(Math.log(number + 1) / Math.log(10));

const findIndexInRanges = (ranges, i) => (ranges || []).findIndex(r => {
  return r.pos[0] <= i && i <= r.pos[1];
})

class SnippetViewer extends Component {
  constructor(props) {
    super(props);
    const colorContinuousScale = scaleOrdinal().range(schemeCategory20);
    this.scaleLineVertPosition = scaleLinear();
    this.scaleLineWidth = scaleLinear();
    this.colorScale = line => {
      const snippetIdx = findIndexInRanges(this.props.snippets, line.pos);
      return snippetIdx < 0 ? COLOR_TRANSPARENT : colorContinuousScale(snippetIdx);
    }
  }

  data() {
    return this.props.lines.map((code, i) => {
      const lineNo = i + 1;
      return {
        code,
        pos: lineNo,
      }
    });
  }

  componentDidMount() {
    this.customRender();
  }

  componentDidUpdate() {
    this.customRender();
  }

  customRender() {
    select(this.node).selectAll('g').remove();

    this.line = select(this.node)
      .selectAll('g')
      .data(this.data.bind(this))
      .enter().append('g');

    this.rect = this.line.append('rect');
    this.rect
      .attr('x', '50px')
      .attr('height', LINE_HEIGHT - 1);

    this.line.append('text')
      .attr('y', LINE_HEIGHT / 2)
      .attr('x', '50px')
      .attr('dy', '.35em')
      .text(line => line.code);

    this.line.append('text')
      .attr('y', LINE_HEIGHT / 2)
      .attr('dy', '.35em')
      .attr('class', 'line-number')
      .text(line => '#' + padd(line.pos, numberLength(this.props.lines.length)) + ' |');

    const height = LINE_HEIGHT * this.props.lines.length;
    this.scaleLineVertPosition
      .domain([1, this.props.lines.length])
      .range([0, height]);
    this.line
      .attr('transform', line => 'translate(0,' + this.scaleLineVertPosition(line.pos) + ')');

    const maxLength = max(this.props.lines, line => line.length);
    const maxWidth = CHAR_WIDTH * maxLength;
    this.scaleLineWidth
      .domain([0, maxLength])
      .range([0, maxWidth]);

    this.rect
      .attr('width', line => this.scaleLineWidth(line.code.length))
      .attr('fill', line => this.colorScale(line));

    selectAll('rect')
      .attr('fill', line => this.colorScale(line));
  }

  render() {
    if (!this.props.lines.length) {
      return null;
    }

    const height = LINE_HEIGHT * this.props.lines.length;
    return <svg
      ref={node => this.node = node}
      width={this.props.width}
      height={height}
    ></svg>
  }
}

export default App;
