import React from 'react'

const UsersCard = ({user}) => {
  return (
    <div className='mx-auto flex flex-row justify-center align-center border border-white py-12 px-2 bg-gray-300'>
        <p>{user.name}</p>
        <p>{user.email}</p>
    </div>
  )
}

export default UsersCard