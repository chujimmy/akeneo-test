import axios from 'axios';
import React from 'react';

interface AddParticipantFormData {
  participantName: string;
  participantEmail: string;
}

interface ParticipantsState {
  participants: Array<{ id: number; name: string; email: string, blacklist: Array<number> }>;
  formData: AddParticipantFormData;
  errorMessageParticipantsList: string;
  errorMessageAddParticipants: string;
  errorMessageBlacklist: string;
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
      errorMessageBlacklist: '',
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

  handleChangeBlacklist = (e: React.ChangeEvent<HTMLInputElement>) => {
    this.setState({ errorMessageBlacklist: '' });

    const { name } = e.target;

    const gifterId = Number(name.split('-')[0]);
    const receiverId = Number(name.split('-')[1]);

    const participant = this.state.participants.find(p => p.id === gifterId );

    if (!participant) {
      return;
    }

    const addToBlacklist = participant.blacklist.indexOf(receiverId) == -1;
    let updatedBlacklist = [...participant.blacklist];

    if (addToBlacklist) {
      updatedBlacklist.push(receiverId);
      axios.post(`http://localhost:8000/participants/${gifterId}/blacklist/${receiverId}`)
        .then(() => {
          this.setState(prevState => ({
            participants: prevState.participants.map((p) => {
              return {
                ...p,
                blacklist: p.id === gifterId ? updatedBlacklist: p.blacklist,
              };
            }),
          }));
        })
        .catch(error => {
          const errorMessage = error.response?.data?.error || 'Could add participant to blacklist';
          this.setState({ errorMessageBlacklist: errorMessage });
        });
    }
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
    const participantsList = this.state.participants.map((participant) => {
      const blacklist = this.state.participants
        .filter((other) => ( other.id !== participant.id ))
        .map((other) => (
          <div>
            <input type="checkbox" onChange={this.handleChangeBlacklist} checked={participant.blacklist.includes(other.id) ? 'checked' : ''} id={participant.id + '-' + other.id} name={participant.id + '-' + other.id}  />
            <label htmlFor={participant.id + '-' + other.id} >{other.name}</label>
          </div>
      ));

      return (
        <li className="participant-list" key={participant.id}>
          {participant.name} ({participant.email} - {participant.id})

          <p>Tick all relevant boxes to ensure the partipant above WILL NOT the selected participants as a gift receiver</p>
          {blacklist}
        </li>
      );
    });

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
          {this.state.errorMessageBlacklist && (
            <div className="error-message" style={{ color: 'red', marginBottom: '10px' }}>
              {this.state.errorMessageBlacklist}
            </div>
          )}
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