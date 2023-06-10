import React from 'react'
import Interval from './interval'

export default function IntervalList({ intervals }) {
  return (
    intervals.map( interval => {
        return <Interval key={interval.id} interval={interval} />
      })
      
  )
}
