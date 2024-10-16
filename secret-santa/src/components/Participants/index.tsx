import axios from 'axios';
import React from 'react';

interface AddParticipantFormData {
  participantName: string;
  participantEmail: string;
}

interface ParticipantsState {
  participants: Array<{ id: number; name: string; email: string }>;
  formData: AddParticipantFormData;
  errorMessage: string;
}

export class Participants extends React.Component<{}, ParticipantsState> {
  constructor(props: {}) {
    super(props);
    this.state = {
      participants: [],
      formData: {
        participantName: '',
        participantEmail: '',
      },
      errorMessage: '',
    };
  }

  componentDidMount() {
    axios.get('http://localhost:8000/participants/')
      .then(res => {
        this.setState({
          participants: res.data.participants,
        });
      })
      .catch(err => {
        console.error('Error fetching participants:', err);
      });
  }

  handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    this.setState(prevState => ({
      formData: {
        ...prevState.formData,
        [name]: value,
      },
      errorMessage: '',
    }));
  };

  handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    axios.post('http://localhost:8000/participants/', {
      name: this.state.formData.participantName,
      email: this.state.formData.participantEmail,
    })
      .then(response => {
        const newParticipant = response.data;

        this.setState(prevState => ({
          participants: [...prevState.participants, newParticipant],
          formData: {
            participantName: '',
            participantEmail: '',
          },
          errorMessage: '',
        }));
      })
      .catch(error => {
        if (error.response && error.response.status === 409) {
          this.setState({ errorMessage: 'Participant already exists.' });
        } else {
          console.error('Error adding participant:', error);
          this.setState({ errorMessage: 'Failed to add participant.' });
        }
      });
  };

  render() {
    const participantsList = this.state.participants.map((p) => (
      <li key={p.id}>{p.name} ({p.email})</li>
    ));

    return (
      <div className="participant">
        <div className="participants-list">
          <h3>Registered participants</h3>
          {this.state.participants.length > 0 && <ul>
            {participantsList}
          </ul>}
          {this.state.participants.length == 0 && <p>No participants to secret santa :(</p>}
        </div>
        {this.state.errorMessage && (
          <div className="error-message" style={{ color: 'red', marginBottom: '10px' }}>
            {this.state.errorMessage}
          </div>
        )}
        <form onSubmit={this.handleSubmit}>
          <h3>Add a new participant</h3>
          <div>
            <label>
              Name:
              <input type="text" name="participantName" value={this.state.formData.participantName} onChange={this.handleChange} required/>
            </label>
          </div>
          <div>
            <label>
              Email:
              <input type="email" name="participantEmail" value={this.state.formData.participantEmail} onChange={this.handleChange} required/>
            </label>
          </div>
          <button type="submit">Submit</button>
        </form>
      </div>
    );
  }
}

export default Participants;