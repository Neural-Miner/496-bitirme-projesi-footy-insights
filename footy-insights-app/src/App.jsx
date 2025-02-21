import './App.css';
import React, { useState, useRef, useEffect } from 'react';
// import videoBg from './assets/background_video_2.mp4'
import videoBg from './assets/background_video.mp4'
import matchesData from './components/matches.json'; // JSON dosyanızı içe aktarın
//import matchDetailsData from './mac_verileri/2017-2018/2017-2018_1_BEŞİKTAŞ A.Ş._ANTALYASPOR A.Ş..json'; // ornek mac detaylari
import matchDetailsData from './components/mac_verileri/2018-2019/2018-2019_10_FENERBAHÇE A.Ş._MKE ANKARAGÜCÜ.json'

import MatchDetails from './MatchDetails';

import { FaPlay, FaPause } from "react-icons/fa"; // oynat-duraklat ikonlari
import { SlArrowLeft } from "react-icons/sl";

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
        <video ref={videoRef} src={videoBg} autoPlay loop muted />
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
  const [showDetails, setShowDetails] = useState(false);
  const [fadeOut, setFadeOut] = useState(false);  // Form'un kaybolma animasyonu icin

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
    setShowDetails(false);
    setFadeOut(false);
  };

  const handleWeekChange = (e) => {
    setSelectedWeek(e.target.value);
    setShowDetails(false);
    setFadeOut(false);
  };

  // Sezon ve hafta secimi sonrasi maclari listele
  useEffect(() => {
    if (selectedSeason && selectedWeek) {
      const matches = matchesData[selectedSeason]?.[selectedWeek] || [];
      setMatchList(matches);
      setSelectedMatch('');
    }
  }, [selectedSeason, selectedWeek]);

  const handleContinue = () => {
    // Form kaybolma animasyonunu baslat
    setFadeOut(true);

    // Animasyon suresi (0.5s) bittikten sonra formu DOM'dan kaldirip detaylari goster
    setTimeout(() => {
      setShowDetails(true);
    }, 500); // CSS'teki fadeOutScale suresine esitleyin
  };

  return (
    <div className="container">
      {/* Form Kapsayici */}
      {!showDetails && (
        <div className={`formWrapper ${fadeOut ? 'fadeOutScale' : 'fadeInScale'}`}>
          <div className="form-group">
            <label className="label" htmlFor="season">Sezon Seç:</label>
            <select
              id="season"
              className="dropdown"
              value={selectedSeason}
              onChange={handleSeasonChange}
            >
              <option value="">Sezon Seçiniz</option>
              {Object.keys(seasonWeekLimits).map((season) => (
                <option key={season} value={season}>{season}</option>
              ))}
            </select>
          </div>

          {selectedSeason && (
            <div className="form-group">
              <label className="label" htmlFor="week">Hafta Seç:</label>
              <select
                id="week"
                className="dropdown"
                value={selectedWeek}
                onChange={handleWeekChange}
              >
                <option value="">Hafta Seçiniz</option>
                {[...Array(seasonWeekLimits[selectedSeason])].map((_, index) => (
                  <option key={index + 1} value={index + 1}>
                    {index + 1}. Hafta
                  </option>
                ))}
              </select>
            </div>
          )}

          {selectedWeek && matchList.length > 0 && (
            <>
              <label className="label">Maç Seç:</label>
              <select
                className="dropdown"
                value={selectedMatch}
                onChange={(e) => setSelectedMatch(e.target.value)}
              >
                <option value="">Maç Seçiniz</option>
                {matchList.map((match, index) => (
                  <option
                    key={index}
                    value={`${match.homeTeam} ${match.homeScore}-${match.awayScore} ${match.awayTeam}`}
                  >
                    {match.homeTeam} | {match.homeScore}-{match.awayScore} | {match.awayTeam}
                  </option>
                ))}
              </select>
            </>
          )}

          {selectedMatch && (
            <button onClick={handleContinue}>Devam</button>
          )}
        </div>
      )}

      {/* Detay Kapsayici */}
      {showDetails && (
        <div className="detailsWrapper fadeInScale">
          <MatchDetails details={matchDetailsData} />
        </div>
      )}
    </div>
  );
};


export default App;