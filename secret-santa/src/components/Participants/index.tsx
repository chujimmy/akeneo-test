import axios from 'axios';
import React from 'react';

export class Participants extends React.Component {
  constructor(props){
    super(props)
    this.state = {
      participants: []
    }
  }

  componentDidMount(){
    axios.get('http://localhost:8000/participants/').then(res => {
      this.setState({
        participants: res.data.participants
      })
    })
  }

  render() {
    const participantsList = this.state.participants.map((p) => <li key={p}>{p}</li>);

    return (
      <div className="shopping-list">
        <h2>Participants</h2>
        <ul>
          {participantsList}
        </ul>
      </div>
    );
  }
}
