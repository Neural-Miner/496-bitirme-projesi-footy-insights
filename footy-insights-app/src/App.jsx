// src/App.jsx
import './App.css';
import React, { useState, useRef, useEffect } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { FaPlay, FaPause, FaArrowRight, FaArrowLeft } from 'react-icons/fa';

import videoBg from './assets/background_video.mp4';
import matchesData from './components/matches_with_paths.json';
import MatchDetails from './MatchDetails';

function App() {
  const videoRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(true);
  const [dimBg, setDimBg] = useState(false);
  const [uploadKey, setUploadKey] = useState(0);

  const handleDimBackground = () => {
    if (videoRef.current) videoRef.current.pause();
    setDimBg(true);
  };

  const togglePlayPause = () => {
    if (videoRef.current.paused) {
      videoRef.current.play();
      setIsPlaying(true);
    } else {
      videoRef.current.pause();
      setIsPlaying(false);
    }
  };

  // Tam sıfırlama: form ve arka plan videosunu yeniden başlatır
  const handleReset = () => {
    setUploadKey(k => k + 1);
    setDimBg(false);
    if (videoRef.current) {
      videoRef.current.play();
      setIsPlaying(true);
    }
  };

  return (
    <div className="App">
      <div className="overlay" />
      <video
        ref={videoRef}
        src={videoBg}
        autoPlay
        loop
        muted
        className={dimBg ? 'videoBg dimVideo' : 'videoBg'}
      />
      <div className="content">
        {/* key değiştiğinde UploadBox yeniden mount olur */}
        <UploadBox
          key={uploadKey}
          onDimBackground={handleDimBackground}
          onReset={handleReset}
        />
      </div>
      <button className="playPauseButton" onClick={togglePlayPause}>
        {isPlaying ? <FaPause /> : <FaPlay />}
      </button>
    </div>
  );
}

const UploadBox = ({ onDimBackground, onReset }) => {
  const [isDownloading, setIsDownloading] = useState(false);
  const [selectedSeason, setSelectedSeason] = useState('');
  const [selectedWeek, setSelectedWeek] = useState('');
  const [matchList, setMatchList] = useState([]);
  const [selectedMatch, setSelectedMatch] = useState('');
  const [showDetails, setShowDetails] = useState(false);
  const [fadeOut, setFadeOut] = useState(false);
  const [matchDetailsLink, setMatchDetailsLink] = useState('');
  const [showMatchDetails, setShowMatchDetails] = useState(true);

  const seasonWeekLimits = Object.fromEntries(
    [...Array(9)].map((_, i) => [`${2011 + i}-${2012 + i}`, 34])
      .concat([
        ['2020-2021', 42],
        ['2021-2022', 38],
        ['2022-2023', 38],
        ['2023-2024', 38],
      ])
  );

  useEffect(() => {
    if (selectedSeason && selectedWeek) {
      const m = matchesData[selectedSeason]?.[selectedWeek] || [];
      setMatchList(m);
      setSelectedMatch('');
      setMatchDetailsLink('');
    }
  }, [selectedSeason, selectedWeek]);

  const handleSeasonChange = e => {
    setSelectedSeason(e.target.value);
    setSelectedWeek('');
    setMatchList([]);
    setSelectedMatch('');
    setShowDetails(false);
    setFadeOut(false);
  };
  const handleWeekChange = e => {
    setSelectedWeek(e.target.value);
    setShowDetails(false);
    setFadeOut(false);
  };
  const handleMatchChange = e => {
    const val = e.target.value;
    setSelectedMatch(val);
    const m = matchList.find(
      mm => `${mm.homeTeam} ${mm.homeScore}-${mm.awayScore} ${mm.awayTeam}` === val
    );
    if (m?.detailsPath) setMatchDetailsLink(m.detailsPath);
  };

  const handleContinue = () => {
    setFadeOut(true);
    setTimeout(() => setShowDetails(true), 500);
  };

  // Geri butonu: tam reset
  const handleBack = () => onReset();

  return (
    <div className="container">
      {/* Sezon/Hafta/Maç formu */}
      {!showDetails && (
        <div className={`formWrapper ${fadeOut ? 'fadeOutScale' : 'fadeInScale'}`}>
          <div className="form-group">
            <label className="label" htmlFor="season">Sezon</label>
            <select
              id="season"
              className="dropdown"
              value={selectedSeason}
              onChange={handleSeasonChange}
            >
              <option value="">Sezon Seçiniz</option>
              {Object.keys(seasonWeekLimits).map(sez => (
                <option key={sez} value={sez}>{sez}</option>
              ))}
            </select>
          </div>

          <AnimatePresence>
            {selectedSeason && (
              <motion.div
                key="week"
                className="form-group"
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.5 }}
                style={{ overflow: 'hidden' }}
              >
                <label className="label" htmlFor="week">Hafta</label>
                <select
                  id="week"
                  className="dropdown"
                  value={selectedWeek}
                  onChange={handleWeekChange}
                >
                  <option value="">Hafta Seçiniz</option>
                  {[...Array(seasonWeekLimits[selectedSeason])].map((_, i) => (
                    <option key={i} value={i+1}>{i+1}. Hafta</option>
                  ))}
                </select>
              </motion.div>
            )}
          </AnimatePresence>

          <AnimatePresence>
            {selectedWeek && matchList.length > 0 && (
              <motion.div
                key="match"
                className="form-group"
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.5 }}
                style={{ overflow: 'hidden' }}
              >
                <label className="label">Maç</label>
                <select
                  className="dropdown"
                  value={selectedMatch}
                  onChange={handleMatchChange}
                >
                  <option value="">Maç Seçiniz</option>
                  {matchList.map((m, i) => (
                    <option
                      key={i}
                      value={`${m.homeTeam} ${m.homeScore}-${m.awayScore} ${m.awayTeam}`}  >
                      {m.homeTeam} | {m.homeScore}-{m.awayScore} | {m.awayTeam}
                    </option>
                  ))}
                </select>
              </motion.div>
            )}
          </AnimatePresence>

          <AnimatePresence>
            {!showDetails && selectedMatch && matchDetailsLink && (
              <motion.button
                key="cont"
                className="continue-button"
                onClick={handleContinue}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.8 }}
                transition={{ duration: 0.25 }}
              >
                <FaArrowRight size="1.2em" />
              </motion.button>
            )}
          </AnimatePresence>
        </div>
      )}

      {/* Maç detayları */}
      {showDetails && matchDetailsLink && (
        <>  
          <div className="detailsWrapper fadeInScale">
            {showMatchDetails && <MatchDetails link={matchDetailsLink} />}
          </div>
          {/* Play Video Button: scrollable olmayan alana taşındı */}
          <DownloadAndPlay
            selectedSeason={selectedSeason}
            selectedWeek={selectedWeek}
            selectedMatch={matchList.find(
              m => `${m.homeTeam} ${m.homeScore}-${m.awayScore} ${m.awayTeam}` === selectedMatch
            )}
            onDownloadStart={() => {
              setShowMatchDetails(false);
              setIsDownloading(true);
            }}
            onDownloadEnd={() => setIsDownloading(false)}
            onDimBackground={onDimBackground}
            isDownloading={isDownloading}
          />

          {/* Geri butonu her zaman reset’e döner */}
          {!isDownloading && (
            <button className="back-button" onClick={handleBack}>
              <FaArrowLeft size="1.5em" />
            </button>
          )}
        </>
      )}
    </div>
  );
};

const DownloadAndPlay = ({
  selectedSeason,
  selectedWeek,
  selectedMatch,
  onDownloadStart,
  onDownloadEnd,
  onDimBackground,
  isDownloading
}) => {
  const [videoUrl, setVideoUrl] = useState(null);

  const handleDownload = async () => {
    if (!selectedSeason || !selectedWeek || !selectedMatch) return;

    onDownloadStart();
    onDimBackground();
    setVideoUrl(null);

    try {
      const res = await fetch('/download-video', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          season: selectedSeason,
          week: selectedWeek,
          homeTeam: selectedMatch.homeTeam,
          awayTeam: selectedMatch.awayTeam,
        }),
      });
      const result = await res.json();
      if (result.success) {
        setVideoUrl(`http://localhost:5000/downloads/${result.videoFileName}`);
      } else {
        alert('Video bulunamadi: ' + result.message);
      }
    } catch (err) {
      console.error(err);
      alert('Sunucu hatasi veya baglanti sorunu.');
    } finally {
      onDownloadEnd();
    }
  };

  return (
    <div>
      {!videoUrl && !isDownloading && (
        <button className="play-video-button" onClick={handleDownload}>
          <FaPlay size="1.2em" />
        </button>
      )}
      {isDownloading && <p>Lütfen bekleyiniz...</p>}
      {videoUrl && (
        <div style={{ height: 'auto' }}>
          <h4>
            {selectedMatch.homeTeam} x {selectedMatch.awayTeam}
          </h4>
          <h3>
            {selectedMatch.homeScore} x {selectedMatch.awayScore}
          </h3>
          <video
            src={videoUrl}
            style={{ width: '90%', height: 'auto' }}
            controls
            autoPlay
          />
        </div>
      )}
    </div>
  );
};

export default App;
