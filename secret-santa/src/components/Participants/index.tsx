import axios from 'axios';
import React from 'react';

interface AddParticipantFormData {
  participantName: string;
  participantEmail: string;
}

interface ParticipantsState {
  participants: Array<{ id: number; name: string; email: string }>;
  formData: AddParticipantFormData;
  errorMessageParticipantsList: string;
  errorMessageAddParticipants: string;
}

export class Participants extends React.Component<object, ParticipantsState> {
  constructor(props: object) {
    super(props);
    this.state = {
      participants: [],
      formData: {
        participantName: '',
        participantEmail: '',
      },
      errorMessageParticipantsList: '',
      errorMessageAddParticipants: '',
    };
  }

  componentDidMount() {
    axios.get('http://localhost:8000/participants/')
      .then(res => {
        this.setState({
          participants: res.data.participants,
        });
      })
      .catch(() => {
        this.setState({errorMessageParticipantsList: 'Error fetching list of participants'});
      });
  }

  handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    this.setState(prevState => ({
      formData: {
        ...prevState.formData,
        [name]: value,
      },
      errorMessageAddParticipants: '',
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
          errorMessageParticipantsList: '',
        }));
      })
      .catch(error => {
        if (error.response && error.response.status === 409) {
          this.setState({ errorMessageAddParticipants: 'Participant already exists.' });
        } else {
          console.error('Error adding participant:', error);
          this.setState({ errorMessageAddParticipants: 'Failed to add participant.' });
        }
      });
  };

  render() {
    const participantsList = this.state.participants.map((p) => (
      <li key={p.id}>{p.name} ({p.email} - {p.id})</li>
    ));

    return (
      <div className="participant">
        <h2>Participants</h2>
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
          {this.state.errorMessageAddParticipants && (
            <div className="error-message" style={{ color: 'red', marginBottom: '10px' }}>
              {this.state.errorMessageAddParticipants}
            </div>
          )}
        </form>


        <div className="participants-list">
          <h3>Registered participants</h3>
          {this.state.participants.length > 0 && <ul>
            {participantsList}
          </ul>}
          {this.state.participants.length == 0 && <p>No participants to secret santa :(</p>}
          {this.state.errorMessageParticipantsList && (
            <div className="error-message" style={{ color: 'red', marginBottom: '10px' }}>
              {this.state.errorMessageParticipantsList}
            </div>
          )}
        </div>
      </div>
    );
  }
}

export default Participants;