import './App.css';
import React, { useState, useRef, useEffect } from 'react';
// import videoBg from './assets/background_video_2.mp4'
import videoBg from './assets/background_video.mp4'
import matchesData from './components/matches.json'; // JSON dosyanızı içe aktarın

import { FaPlay, FaPause } from "react-icons/fa"; // oynat-duraklat ikonlari

function App() {

  const videoRef = useRef(null); // video kontrolu
  const [isPlaying, setIsPlaying] = useState(true);

  const togglePlayPause = () => {
    if (videoRef.current.paused) {
      videoRef.current.play();
      setIsPlaying(true);
    } else {
      videoRef.current.pause();
      setIsPlaying(false);
    }
  };


  return (
    <div className="App">
      <div className="overlay"></div>
        <video src={videoBg} autoPlay loop muted />
          <div className="content">
            <UploadBox />
          </div>
      <button className="playPauseButton" onClick={togglePlayPause}>
        {isPlaying ? <FaPause /> : <FaPlay />}
      </button>
    </div>
  );
}

const UploadBox = () => {

  const [video, setVideo] = useState(null);

  const handleVideoUpload = (e) => {
    setVideo(e.target.files[0]);
    alert(`${e.target.files[0].name} yüklendi!`);
  };

  const [selectedSeason, setSelectedSeason] = useState('');
  const [selectedWeek, setSelectedWeek] = useState('');
  const [matchList, setMatchList] = useState([]);
  const [selectedMatch, setSelectedMatch] = useState('');

  const seasonWeekLimits = Object.fromEntries(
    [...Array(9)].map((_, i) => [`${2011 + i}-${2012 + i}`, 34])
      .concat([
        ['2020-2021', 42],
        ['2021-2022', 38],
        ['2022-2023', 38],
        ['2023-2024', 38],
      ])
  );

  const handleSeasonChange = (e) => {
    const season = e.target.value;
    setSelectedSeason(season);
    setSelectedWeek('');
    setMatchList([]);
    setSelectedMatch('');
  };

  const handleWeekChange = (e) => {
    setSelectedWeek(e.target.value);
  };

  // Sezon ve hafta secimi sonrasi maclari listele
  useEffect(() => {
    if (selectedSeason && selectedWeek) {
      const matches = matchesData[selectedSeason]?.[selectedWeek] || [];
      setMatchList(matches);
      setSelectedMatch('');
    }
  }, [selectedSeason, selectedWeek]);

  return (
    <div className="container">

      <div className="form-group">
        <label className="label" htmlFor="season">Sezon Seç:</label>
        <select id="season" className="dropdown" value={selectedSeason} onChange={handleSeasonChange}>
          <option value="">Sezon Seçiniz</option>
          {Object.keys(seasonWeekLimits).map((season) => (
            <option key={season} value={season}>{season}</option>
          ))}
        </select>
      </div>

      {selectedSeason && (
        <div className="form-group">
          <label className="label" htmlFor="week">Hafta Seç:</label>
          <select id="week" className="dropdown" value={selectedWeek} onChange={handleWeekChange}>
            <option value="">Hafta Seçiniz</option>
            {[...Array(seasonWeekLimits[selectedSeason])].map((_, index) => (
              <option key={index + 1} value={index + 1}>{index + 1}. Hafta</option>
            ))}
          </select>
        </div>
      )}

      {selectedWeek && matchList.length > 0 && (
        <>
          <label className="label">Maç Seç:</label>
          <select className="dropdown" value={selectedMatch} onChange={(e) => setSelectedMatch(e.target.value)}>
            <option value="">Maç Seçiniz</option>
            {matchList.map((match, index) => (
              <option key={index} value={`${match.homeTeam} ${match.homeScore}-${match.awayScore} ${match.awayTeam}`}>
                {match.homeTeam} | {match.homeScore}-{match.awayScore} | {match.awayTeam}
              </option>
            ))}
          </select>
        </>
      )}

      {/*
      {selectedMatch && (
        <div className="selected-match">
          <h3>Seçilen Maç:</h3>
          <p>{selectedMatch}</p>
        </div>
      )}
      */}




      {/*
      <div className="form-group">
          <label className="label" htmlFor="videoUpload">
            Maç videosunu yükleyiniz:
          </label>
          <input type="file" id="video" accept="video/*" className="input" onChange={handleVideoUpload}/>
      </div>
      */}

      {/*
      <div>
        <label className='label' htmlFor='homeTeam'>
          Ev Sahibi Takım:
        </label>
        <input type='text' id='homeTeam' placeholder='Ev sahibi takımı giriniz' className='input'/>
      </div>

      <div>
        <label className='label' htmlFor='awayTeam'>
          Deplasman Takımı:
        </label>
        <input type='text' id='awayTeam' placeholder='Deplasman takımı giriniz' className='input'/>
      </div>
      */}

      {/*
      <div className="form-group">
          <label className="label" htmlFor="season">
            Sezon:
          </label>
          <input type="text" id="season" placeholder="(örn. 2023-2024)" className="input"
          />
      </div>

        <div className="form-group">
          <label className="label" htmlFor="week">
            Hafta:
          </label>
          <input type="number" id="week" placeholder="(örn. 8)" min={1}
            className="input"
          />
        </div>
        */}     

    </div>
  );



};

export default App;