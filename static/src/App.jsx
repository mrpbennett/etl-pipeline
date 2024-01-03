import {useEffect, useState} from 'react'
import Postgres from './assets/postgresql.svg'
import Redis from './assets/redis.svg'

function App() {
  const [users, setUsers] = useState([])
  const [user, setUser] = useState([])

  const getUser = async userID => {
    await fetch(`http://127.0.0.1:8000/api/datapipe/${userID}`)
      .then(response => response.json())
      .then(data => setUser(data))
      .catch(error => console.error(error))
  }

  useEffect(() => {
    // generate a list of users on mount
    fetch(`http://127.0.0.1:8000/api/datapipe/list-users`)
      .then(response => response.json())
      .then(data => setUsers(data))
      .catch(error => console.error(error))
  }, [])

  const renderUserData = () => {
    if (Array.isArray(user)) {
      // Handle rendering for postgres_data (array)
      return user.map((userArray, index) => (
        <>
          <div className="flex items-center mb-4">
            <p className="mr-4">Data found in:</p>
            <img src={Postgres} width={50} className="align-middle" />
          </div>

          <div
            key={index}
            className="rounded-md border border-gray-300 bg-gray-600 p-4 font-mono text-white"
          >
            {userArray.map((item, itemIndex) => (
              <p key={itemIndex}>{item}</p>
            ))}
          </div>
        </>
      ))
    } else {
      // Handle rendering for redis_data (object)
      return (
        <>
          <div className="flex items-center mb-4">
            <p className="mr-4">Data found in:</p>
            <img src={Redis} width={50} className="align-middle" />
          </div>
          <div className="rounded-md border border-gray-300 bg-gray-600 p-4 font-mono text-white">
            {Object.entries(user).map(([key, value], index) => (
              <p key={index}>{`${key}: ${value}`}</p>
            ))}
          </div>
        </>
      )
    }
  }

  return (
    <div className="container mx-auto max-w-[960px] overflow-auto">
      <div>
        <p className="mt-8 text-lg">
          Click on the <code>uid</code> to display the relevant data for that
          user...
        </p>
      </div>
      <div className="grid grid-cols-2 gap-4 mt-10">
        <div>
          <h1 className="font-bold mb-4">
            Current user <code>uid</code>s
          </h1>
          {users.map(item => (
            <ol key={item}>
              <li
                key={item}
                className="font-mono hover:cursor-pointer hover:text-blue-500"
                onClick={() => getUser(item)}
              >
                {item}
              </li>
            </ol>
          ))}
        </div>
        <div className="sticky top-0">
          <h1 className="font-bold mb-4">User data</h1>
          <div>{renderUserData()}</div>
        </div>
      </div>
    </div>
  )
}

export default App
