import axios from 'axios';
import React from 'react';

const DRAWS_HISTORY_LIMIT = 5;

interface DrawDetailParticipant {
  id: number;
  name: string;
  email: string;
}

interface DrawsState {
  draws: Array<{ 
    id: number;
    created: string;
    details : Array<{gifter: DrawDetailParticipant; receiver:DrawDetailParticipant}>;
  }>;
  errorMessageNewDraw: string;
  errorMessagePreviousDraws: string;
}

export class Draws extends React.Component<object, DrawsState> {
  constructor(props: object) {
    super(props);
    this.state = {
      draws: [],
      errorMessageNewDraw: '',
      errorMessagePreviousDraws: '',
    };
  }

  componentDidMount() {
    axios.get(`http://localhost:8000/draws?limit=${DRAWS_HISTORY_LIMIT}`)
      .then(res => {
        this.setState({
          draws: res.data.draws,
        });
      })
      .catch(() => {
        this.setState({ errorMessagePreviousDraws: 'Error fetching latest draws' });
      });
  }

  handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    axios.post('http://localhost:8000/draws/')
      .then(response => {
        const newDraw = response.data;

        this.setState(prevState => ({
          draws: [newDraw, ...prevState.draws].slice(0, DRAWS_HISTORY_LIMIT),
          errorMessageNewDraw: '',
          errorMessagePreviousDraws: '',
        }));
      })
      .catch(error => {
        const errorMessage = error.response?.data?.error || 'Could not make a new draw';
        this.setState({ errorMessageNewDraw: errorMessage });
      });
  };

  render() {
    const draws = this.state.draws.map((draw) => {
      const drawDetail = draw.details.map((detail) => (
        <span className="draw-detail" key={draw.id + detail.gifter.name + detail.receiver.name}>
          {detail.gifter.name} will give a gift to {detail.receiver.name}
        </span>
      ));
  
      return (
        <li className="draw" key={draw.id}>
          Draw id {draw.id} (created on {draw.created})
          <div>{drawDetail}</div>
        </li>
      );
    });
  
    return (
      <div className="draws">
        <h2>Draw</h2>
        <form onSubmit={this.handleSubmit}>
          <h3>Make a new draw</h3>
          <button type="submit">Draw!</button>
        </form>

        {this.state.errorMessageNewDraw && (
          <div className="error-message" style={{ color: 'red', marginBottom: '10px' }}>
            {this.state.errorMessageNewDraw}
          </div>
        )}

        <div className="previous-draws">
          <h3>Previous draws (last {DRAWS_HISTORY_LIMIT})</h3>
          {this.state.errorMessagePreviousDraws && (
            <div className="error-message" style={{ color: 'red', marginBottom: '10px' }}>
              {this.state.errorMessagePreviousDraws}
          </div>
          )}
          {this.state.draws.length > 0 && (
            <ul>
              {draws}
            </ul>
          )}
          {this.state.draws.length == 0 && !this.state.errorMessagePreviousDraws && <p>There is no draws at the moment</p>}
        </div>
      </div>
    );
  }
}

export default Draws;
