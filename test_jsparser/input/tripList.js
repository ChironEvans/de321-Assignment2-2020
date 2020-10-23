/* globals localStorage */
/* eslint-disable eqeqeq, no-unused-vars, prefer-const, no-useless-return */
const STORAGE_KEY = 'tripListCME'


// FEATURE 1: Create a whole that acts as a facade for parts
class TripList {
  constructor () {
    this.allMyTrips = []
    this.editingTrip = null
    this.editCache = null
    this.editType = null
    this.sortType = ''
    this.comparitors = {
      '<': function (a, b) { return a < b },
      '<=': function (a, b) { return a <= b },
      '>': function (a, b) { return a > b },
      '>=': function (a, b) { return a >= b },
      '=': function (a, b) { return a === b },
      '!=': function (a, b) { return a !== b }
    }
    this.tripFetch = {
      id: function (trip) { return trip.id },
      time: function (trip) { return trip.time },
      distance: function (trip) { return trip.distance },
      duration: function (trip) { return trip.duration }
    }
  }

  // FEATURE 7: Load all parts from LocalStorage
  load () {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
  }

  // FEATURE 6: Save all parts to LocalStorage
  save () {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(this.allMyTrips))
  }

  // FEATURE 2: Add a Part
  addTrip (newTripTime, newTripDistance, newTripDuration) {
    let newTripDateTime = new Date(newTripTime)
    // FEATURE 10: Validate inputs
    // Check if the date given is valid
    if (newTripDateTime == 'Invalid Date') {
      return
    }
    // check that the distance is not 0
    // distance can only be a number input, handled through HTML field
    if (newTripDistance <= 0) {
      return
    }
    // check that the duration is not 0
    // distance can only be a whole number input, handled through HTML field
    if (newTripDuration <= 0) {
      return
    } else { // If all fields are valid add the trip
      // FEATURE 13: Provide default values
      // ID value automatically assigned
      const newID = this.allMyTrips.length + 1
      const aNewTrip = new Trip(newID, newTripTime, newTripDistance, newTripDuration)
      this.allMyTrips.push(aNewTrip)
    }
  }

  // Returns a data value from all trips in an array
  getTripData (arr, type) {
    const returnArr = []
    for (const trip of arr) {
      returnArr.push(this.tripFetch[type](trip))
    }
    return returnArr
  }

  // FEATURE 3: sort parts
  // Sorts parts by any given data type using a merge sort algorithm
  sortTrips (type) {
    this.sortType = type
    const sortedTrips = this.mergeSort(this.allMyTrips)
    this.allMyTrips = sortedTrips
  }

  merge (left, right) {
    // Initialize a sorted array and indexes to increment through l & r
    const resultArray = []
    let leftIndex = 0
    let rightIndex = 0

    // Concat values into resultArray
    while (leftIndex < left.length && rightIndex < right.length) {
      // Check which value being sorted by is higher
      // add the lower to the array, increment the index of the side that was added
      if (this.tripFetch[this.sortType](left[leftIndex]) < this.tripFetch[this.sortType](right[rightIndex])) {
        resultArray.push(left[leftIndex])
        leftIndex++
      } else {
        resultArray.push(right[rightIndex])
        rightIndex++
      }
    }
    // ensure that the left over item(s) are added to the array before being returned
    return resultArray
      .concat(left.slice(leftIndex))
      .concat(right.slice(rightIndex))
  }

  mergeSort (arr) {
    // Recursively split and merge the array
    if (arr.length <= 1) {
      return arr
    }
    const midpoint = Math.floor(arr.length / 2)

    const left = arr.slice(0, midpoint)
    const right = arr.slice(midpoint)

    return this.merge(
      this.mergeSort(left), this.mergeSort(right)
    )
  }

  // FEATURE 15: get all parts
  getAllTrips () {
    return this.allMyTrips
  }

  // FEATURE 4: Filter parts
  // Filters the trips using a number of given operators and conditions (e.g. filter parts by distance > 20)
  // FEATURE 14: Find a part given a search criterion
  // The '=' operator can be used to search for a specific trip using the time or id field
  filterTrips (type, operator, value) {
    // Would like to solve this...currently unable to have the filter read values from tripList obj
    // Read comparitors from the tripList obj tp make them available to the filter
    const comparitors = this.comparitors
    const tripFetch = this.tripFetch
    // Gets which function to perform based on the operator variable passed from a controller
    const filteredArr = this.allMyTrips.filter(function (trip) {
      // function to take the type variable and fetch trip data based on the input
      return (comparitors[operator](tripFetch[type](trip), value))
    })
    return filteredArr
  }

  // FEATURE 8: Update/Edit a part
  // The proposed edit is stored in the variable editCache and the edit is only actioned on a confirmEdit call
  editTrip (trip, type, value) {
    this.editCache = value
    this.editType = type
    this.editingTrip = trip
  }

  confirmEdit () {
    // Check that there is a trip being edited
    if (!this.editingTrip) {
      return
    }

    // Check for what kind of input is being given, apply validation
    switch (this.editType) {
      case 'distance': {
        if (this.editCache > 0) {
          this.editingTrip.distance = this.editCache
        }
        break
      }
      case 'time': {
        let editTripDateTime = ''
        try { editTripDateTime = new Date(this.editCache) } finally {
          if (editTripDateTime !== 'Invalid Date') {
            this.editingTrip.time = this.editCache
          }
        }
        break
      }
      case 'duration': {
        if (this.editCache > 0) {
          this.editingTrip.duration = this.editCache
        }
        break
      }
    }
    this.editCache = null
    this.editType = null
  }

  // FEATURE 9: Discard/revert edits to a part
  cancelEdit () {
    this.editCache = null
    this.editingTrip = null
    this.editType = null
  }

  // FEATURE 5: Delete a selected part
  removeTrip (trip) {
    const i = this.allMyTrips.indexOf(trip)
    this.allMyTrips.splice(i, 1)
  }

  // FEATURE 11: A calculation within a part
  getAvgSpeed (trip) {
    // Gets average speed in km/h, duration is in minutes
    const avgSpeed = ((trip.distance / trip.duration) * 60)
    return avgSpeed
  }

  // FEATURE 12: A calculation across many parts
  getAllAvgSpeed (arr) {
    let totalSpeed = 0
    let allAvgSpeed = 0
    for (const trip of arr) {
      totalSpeed += this.getAvgSpeed(trip)
    }
    allAvgSpeed = totalSpeed / arr.length
    return allAvgSpeed
  }
}
