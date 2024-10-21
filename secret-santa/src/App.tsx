import { Draws } from './components/Draws';
import { Participants } from './components/Participants';

function App() {
  return (
    <>
      <h1>Secret Santa</h1>
      <Participants/>
      <hr/>
      <Draws/>
    </>
  )
}

export default App
