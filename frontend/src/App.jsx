import { useEffect, useState } from 'react'
import './App.css'

const API_URL = 'http://localhost:8000'

function App() {
  const [selectedDate, setSelectedDate] = useState('')
  const [availableTimes, setAvailableTimes] = useState([])
  const [selectedTime, setSelectedTime] = useState('')
  const [loading, setLoading] = useState(false)
  const [booking, setBooking] = useState(false)
  const [error, setError] = useState('')
  const [confirmation, setConfirmation] = useState(null)

  useEffect(() => {
    if (!selectedDate) {
      return
    }

    async function fetchAvailableTimes() {
      setLoading(true)
      setError('')

      try {
        const response = await fetch(
          `${API_URL}/available?date=${selectedDate}`
        )

        if (!response.ok) {
          throw new Error('Não foi possível consultar os horários.')
        }

        const data = await response.json()

        setAvailableTimes(data.available_times)
      } catch {
        setAvailableTimes([])
        setError('Não foi possível consultar os horários disponíveis.')
      } finally {
        setLoading(false)
      }
    }

    fetchAvailableTimes()
  }, [selectedDate])

  async function handleAppointment() {
    setBooking(true)
    setError('')

    try {
      const response = await fetch(`${API_URL}/appointments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          date: selectedDate,
          time: selectedTime,
        }),
      })

      if (!response.ok) {
        const data = await response.json()

        throw new Error(
          data.detail || 'Não foi possível realizar o agendamento.'
        )
      }

      const data = await response.json()

      setConfirmation(data)

      setAvailableTimes((times) =>
        times.filter((time) => time !== selectedTime)
      )

      setSelectedTime('')
    } catch (error) {
      setError(error.message)
    } finally {
      setBooking(false)
    }
  }

  function formatDate(date) {
    return new Intl.DateTimeFormat('pt-BR').format(
      new Date(`${date}T00:00:00`)
    )
  }

  return (
    <main className="appointment-page">
      <section className="appointment-card">
        <header className="appointment-header">
          <h1>Agendamento</h1>

          <p>Escolha uma data e um horário disponível.</p>
        </header>

        <div className="appointment-content">
          <div className="date-section">
            <label htmlFor="date">Data</label>

            <input
              id="date"
              type="date"
              lang="pt-BR"
              value={selectedDate}
              onChange={(event) => {
                const date = event.target.value

                setSelectedDate(date)
                setSelectedTime('')
                setConfirmation(null)
                setError('')

                if (!date) {
                  setAvailableTimes([])
                }
              }}
            />
          </div>

          <div className="times-section">
            <h2>Horários disponíveis</h2>

            {!selectedDate && (
              <p className="empty-message">
                Selecione uma data para visualizar os horários disponíveis.
              </p>
            )}

            {loading && (
              <p className="empty-message">
                Consultando horários...
              </p>
            )}

            {error && (
              <p className="error-message">
                {error}
              </p>
            )}

            {!loading &&
              !error &&
              selectedDate &&
              availableTimes.length === 0 && (
                <p className="empty-message">
                  Não há horários disponíveis para esta data.
                </p>
              )}

            {!loading && !error && availableTimes.length > 0 && (
              <div className="time-list">
                {availableTimes.map((time) => (
                  <button
                    key={time}
                    type="button"
                    className={selectedTime === time ? 'selected' : ''}
                    onClick={() => setSelectedTime(time)}
                  >
                    {time.slice(0, 5)}
                  </button>
                ))}
              </div>
            )}

            {selectedTime && (
              <div className="confirmation-section">
                <p>
                  Horário selecionado:{' '}
                  <strong>{selectedTime.slice(0, 5)}</strong>
                </p>

                <button
                  type="button"
                  onClick={handleAppointment}
                  disabled={booking}
                >
                  {booking
                    ? 'Agendando...'
                    : 'Confirmar agendamento'}
                </button>
              </div>
            )}

            {confirmation && (
              <div className="success-message">
                <h2>Agendamento realizado!</h2>

                <p>
                  Data:{' '}
                  <strong>{formatDate(confirmation.date)}</strong>
                </p>

                <p>
                  Horário:{' '}
                  <strong>{confirmation.time.slice(0, 5)}</strong>
                </p>
              </div>
            )}
          </div>
        </div>
      </section>
    </main>
  )
}

export default App