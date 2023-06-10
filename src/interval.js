import React from 'react'

export default function interval({ interval }) {
    
   

    return (
        <div>
            <label>{interval.name}</label>
            <label>{interval.sumMinutes}</label>
        </div>
    )
}