import React from "react";
import ReactDOM from "react-dom";
import "./index.css";

function Square(props) {
  return (
    <button className="square" onClick={props.onClick}>
      {props.inWin ? <b>{props.value}</b> : props.value}
    </button>
  );
}

class Board extends React.Component {
  renderSquare(i) {
    const inWin = this.props.winLine.includes(i);
    const sign = this.props.squares[i];

    return (
      <Square
        value={sign}
        onClick={() => this.props.onClick(i)}
        inWin={inWin}
      />
    );
  }

  render() {
    const rows = [0, 1, 2].map((i) => (
      <div className="board-row" key={i}>
        {this.renderSquare(i * 3)}
        {this.renderSquare(i * 3 + 1)}
        {this.renderSquare(i * 3 + 2)}
      </div>
    ));
    return <div>{rows}</div>;
  }
}

class Game extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      history: [
        {
          squares: Array(9).fill(null),
          move: null,
        },
      ],
      stepNumber: 0,
      xIsNext: true,
      ascending: true,
    };
  }

  handleClick(i) {
    const history = this.state.history.slice(0, this.state.stepNumber + 1);
    const current = history[this.state.stepNumber];
    const squares = current.squares.slice();
    if (calculateWinner(squares) || squares[i]) {
      return;
    }
    squares[i] = this.state.xIsNext ? "X" : "O";
    this.setState({
      history: history.concat([
        {
          squares: squares,
          move: i,
        },
      ]),
      stepNumber: history.length,
      xIsNext: !this.state.xIsNext,
    });
  }

  jumpTo(step) {
    this.setState({
      stepNumber: step,
      xIsNext: step % 2 === 0,
    });
  }

  render() {
    const history = this.state.history;
    const current = history[this.state.stepNumber];
    const winner = calculateWinner(current.squares);
    const winLine = (winner || {}).line || [];

    const moves = history.map((step, move) => {
      const desc = move
        ? `Go to move #${move} (${1 + ~~(step.move / 3)}, ${
            (step.move % 3) + 1
          })`
        : "Go to game start";
      return (
        <li key={move}>
          <button onClick={() => this.jumpTo(move)}>
            {this.state.stepNumber === move ? <b>{desc}</b> : desc}
          </button>
        </li>
      );
    });

    let status;
    if (winner) {
      status = winner === "Draw" ? "Draw! -_-" : "Winner: " + winner.sign;
    } else {
      status = "Next player: " + (this.state.xIsNext ? "X" : "O");
    }

    return (
      <div className="game">
        <div className="game-board">
          <Board
            squares={current.squares}
            onClick={(i) => this.handleClick(i)}
            winLine={winLine}
          />
        </div>
        <div className="game-info">
          <div>{status}</div>
          <div>
            <button
              onClick={() =>
                this.setState({ ascending: !this.state.ascending })
              }
            >
              {this.state.ascending ? "↓" : "↑"}
            </button>
          </div>
          <ul>{this.state.ascending ? moves : moves.reverse()}</ul>
        </div>
      </div>
    );
  }
}

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return {sign: squares[a], line: lines[i]};
    }
  }

  if (squares.some((s) => !s)) {
    return null;
  } else {
    return "Draw";
  }
}

// ========================================

ReactDOM.render(<Game />, document.getElementById("root"));
