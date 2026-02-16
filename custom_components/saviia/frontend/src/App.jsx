import { useState } from 'react'
import './App.css'

export default function App({ hass }) {
  const createTask = async () => {
    const result = await hass.callService(
      "saviia",
      "create_task",
      { title: "React works" },
      { returnResponse: true }
    );

    console.log(result);
  };

  return (
    <div>
      <h1>SAVIIA React 🚀</h1>
      <button onClick={createTask}>Create Task</button>
    </div>
  );
}
