const STORAGE_KEY = 'tripListCME'

class Trip {
    public id: number
    public time: String
    public distance: number
    public duration: number

    constructor(tripID: number, tripTime: String, tripDistance: number, tripDuration: number) {
        this.id = tripID
        this.time = tripTime
        this.distance = tripDistance
        this.duration = tripDuration
    }
}

class TripList {
    private allMyTrips: Array<Trip>
    private editingTrip: Trip
    private editCache: any
    private editType: string
    private sortType: string
    private comparitors: { [elementType: string]: (a: any, b: any) => boolean; };
    private tripFetch: { [elementType: string]: (trip: Trip) => {}; };
    
    constructor() {
        this.allMyTrips = []
        this.editingTrip = undefined
        this.editCache = undefined
        this.editType = undefined
        this.sortType = undefined
        this.comparitors = {
          '<':  (a, b) => { return a < b },
          '<=':  (a, b) => { return a <= b },
          '>':  (a, b) => { return a > b },
          '>=':  (a, b) => { return a >= b },
          '=':  (a, b) => { return a === b },
          '!=':  (a, b) => { return a !== b }
        }
        this.tripFetch = {
          'id':  (trip: { id: number }) => { return trip.id },
          'time':  (trip: { time: any }) => { return trip.time },
          'distance':  (trip: { distance: number }) => { return trip.distance },
          'duration':  (trip: { duration: number }) => { return trip.duration },
          'speed': (trip) => { let avgSpeed: number = ((trip.distance / trip.duration) * 60)
            return avgSpeed } 
        }
    }
    public load() {
        return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
    }

    public save () {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(this.allMyTrips))
    }

    public addTrip (newTripTime: string, newTripDistance: number, newTripDuration: number) {
        let newTripDateTime = new Date(newTripTime)
        // Check if the date given is valid
        if (newTripDateTime.toString() == 'Invalid Date') {
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
          // ID value automatically assigned
          const newID = this.allMyTrips.length + 1
          const aNewTrip = new Trip(newID, newTripTime, newTripDistance, newTripDuration)
          this.allMyTrips.push(aNewTrip)
        }
      }
    
  // Returns a data value from all trips in an array
  getTripData (arr: any, type: string | number) {
    const returnArr = []
    for (const trip of arr) {
      returnArr.push(this.tripFetch[type](trip))
    }
    return returnArr
  }

  sortTrips (type: string) {
    var tripFetch = this.tripFetch;
    let sortedArr = this.allMyTrips.sort(function (a,b) {
        let x: any = tripFetch[type](a)
        let y: any = tripFetch[type](b)
        if (type == 'time') {
            return x<y ? -1 : x>y ? 1 : 0;
        }
        else {return x - y}
        
    })
    return sortedArr
}

  getAllTrips () {
    return this.allMyTrips
  }

  // Filters the trips using a number of given operators and conditions (e.g. filter parts by distance > 20)
  // The '=' operator can be used to search for a specific trip using the time or id field
  filterTrips (type: string | number, operator: string | number, value: any) {
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

  // The proposed edit is stored in the variable editCache and the edit is only actioned on a confirmEdit call
  editTrip (trip: Trip, type: string, value: any) {
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
        let editTripDateTime = null
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

  cancelEdit () {
    this.editCache = null
    this.editingTrip = null
    this.editType = null
  }

  removeTrip (trip: Trip) {
    const i = this.allMyTrips.indexOf(trip)
    this.allMyTrips.splice(i, 1)
  }

  getAllAvgSpeed (arr: Trip[]) {
    let totalSpeed: number = 0
    let allAvgSpeed: number = 0
    for (const trip of arr) {
      totalSpeed += this.getTripData(trip, 'time')[0]
    }
    allAvgSpeed = totalSpeed / arr.length
    return allAvgSpeed
  }
}