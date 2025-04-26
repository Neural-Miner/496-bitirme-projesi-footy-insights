// src/App.jsx
import './App.css';
import React, { useState, useRef, useEffect } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { FaPlay, FaPause, FaArrowRight, FaArrowLeft } from 'react-icons/fa';

import videoBg from './assets/background_video.mp4';
import matchesData from './components/matches_with_paths.json';
import MatchDetails from './components/MatchDetails';

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
  const [matchDetailsLink, setMatchDetailsLink] = useState('');

  const [showDetails, setShowDetails] = useState(false);
  // const [showVoiceSelect, setShowVoiceSelect] = useState(false);
  // const [selectedVoice, setSelectedVoice] = useState('');
  // const [voiceConfirmed, setVoiceConfirmed] = useState(false);

  const [canDownload, setCanDownload] = useState(false);

  // const voiceOptions = [
  //   { value: 'voice1', label: 'Spiker 1' },
  //   { value: 'voice2', label: 'Spiker 2' },
  //   { value: 'voice3', label: 'Spiker 3' },
  // ];

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
      // reset downstream stages
      setShowDetails(false);
      // setShowVoiceSelect(false);
      // setSelectedVoice('');
      // setVoiceConfirmed(false);
    }
  }, [selectedSeason, selectedWeek]);

  const handleSeasonChange = e => {
    setSelectedSeason(e.target.value);
    setSelectedWeek('');
  };
  const handleWeekChange = e => {
    setSelectedWeek(e.target.value);
  };
  const handleMatchChange = e => {
    const val = e.target.value;
    setSelectedMatch(val);
    const m = matchList.find(
      mm => `${mm.homeTeam} ${mm.homeScore}-${mm.awayScore} ${mm.awayTeam}` === val
    );
    if (m?.detailsPath) {
      // public/mac_verileri altından okunacak şekilde normalize et (başındaki “/” işareti çıkarılıyor)
      setMatchDetailsLink(m.detailsPath.replace(/^\/+/, ''));
    }
  };

  const handleToDetails = () => {
    setShowDetails(true);
  };
  // const handleToVoiceSelect = () => {
  //   setShowVoiceSelect(true);
  // };
  // const handleVoiceConfirm = () => {
  //   setVoiceConfirmed(true);
  // };

  const handleToDownload = () => {
    setCanDownload(true);
  }

  const handleBack = () => {
    onReset();
  };

  return (
    <div className="container">
      {/* 1) Maç seçimi */}
      {!showDetails && (
        <div className="formWrapper fadeInScale">
          {/* Sezon */}
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
          {/* Hafta */}
          <AnimatePresence>
            {selectedSeason && (
              <motion.div
                className="form-group"
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
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
                    <option key={i} value={i+1}>{i+1}</option>
                  ))}
                </select>
              </motion.div>
            )}
          </AnimatePresence>
          {/* Maç */}
          <AnimatePresence>
            {selectedWeek && matchList.length > 0 && (
              <motion.div
                className="form-group"
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
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
                      value={`${m.homeTeam} ${m.homeScore}-${m.awayScore} ${m.awayTeam}`}
                    >
                      {m.homeTeam} | {m.homeScore}-{m.awayScore} | {m.awayTeam}
                    </option>
                  ))}
                </select>
              </motion.div>
            )}
          </AnimatePresence>
          {/* Continue */}
          <AnimatePresence>
            {selectedMatch && matchDetailsLink && (
              <motion.button
                className="continue-button"
                onClick={handleToDetails}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.8 }}
                transition={{ duration: 0.2 }}
              >
                <FaArrowRight />
              </motion.button>
            )}
          </AnimatePresence>
        </div>
      )}

      {/* 2) Maç Detayları + Continue */}
      {showDetails && !canDownload && (
        <>
        <button className="back-button-details" onClick={handleBack}>
            <FaArrowLeft />
        </button>
        <div className="detailsWrapper fadeInScale">
          <MatchDetails link={matchDetailsLink} />
        </div>
        <button className="play-video-button" onClick={handleToDownload}>
          <FaPlay />
        </button>
        </>
      )}

      {/* 3) Spiker Seçimi + Continue */}
      {/* {showDetails && showVoiceSelect && !voiceConfirmed && (
        <>
        <motion.div
          className="formWrapper"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          transition={{ duration: 0.3 }}
          style={{ transformOrigin: 'top center' }}
        >
          <div className="form-group">
            <label className="label" htmlFor="voice">Spiker Seçimi</label>
            <select
              id="voice"
              className="dropdown"
              value={selectedVoice}
              onChange={e => setSelectedVoice(e.target.value)}
            >
              <option value="">Seçiniz</option>
              {voiceOptions.map(opt => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>
          <button
            className="play-video-button"
            disabled={!selectedVoice}
            onClick={handleVoiceConfirm}
          >
            <FaPlay />
          </button>
          <button
            className="back-button-spiker"
            onClick={handleBack}
          >
            <FaArrowLeft />
          </button>
        </motion.div>
        </>
      )} */}

      {/* 4) DownloadAndPlay */}
      {showDetails && canDownload && (
        <>
          <DownloadAndPlay
            selectedSeason={selectedSeason}
            selectedWeek={selectedWeek}
            selectedMatch={selectedMatch}
            onDownloadStart={() => setIsDownloading(true)}
            onDownloadEnd={() => setIsDownloading(false)}
            onDimBackground={onDimBackground}
            isDownloading={isDownloading}
          />
        </>
      )}
      {showDetails && canDownload && (
        <button className="back-button" onClick={handleBack}>
          <FaArrowLeft />
        </button>
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
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  useEffect(() => {
    handleDownload();
  }, []);

  const handleDownload = async () => {
    if (!selectedSeason || !selectedWeek || !selectedMatch) return;

    onDownloadStart();
    onDimBackground();
    setVideoUrl(null);

    let fileName, alreadyExists=false;
    try {
      const res = await fetch('/download-video', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          season: selectedSeason,
          week: selectedWeek,
          homeTeam: selectedMatch.split(' ')[0],
          awayTeam: selectedMatch.split(' ').slice(-1)[0],
        }),
      });
      const result = await res.json();
      alreadyExists = result.message === 'Dosya zaten mevcut';
      fileName = result.videoFileName;
      setVideoUrl(`http://localhost:5000/downloads/${fileName}`);
      
      console.log("download-video body:", {
        season: selectedSeason,
        week: selectedWeek,
        homeTeam: selectedMatch.split(' ')[0],
        awayTeam: selectedMatch.split(' ').slice(-1)[0]
      });

    } catch {
      alert('Video indirme hatasi');
      onDownloadEnd();
      return;
    }

    if (!alreadyExists) {
      setIsAnalyzing(true);
      try {
        await fetch('/predict-video', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ videoFileName: fileName }),
        });
      } catch {
        /* keep message visible */
      }
      setIsAnalyzing(false);
    }
    onDownloadEnd();
  };

  return (
    <div className="playWrapper">
      {!videoUrl && !isDownloading && (
        <button className="play-video-button" onClick={handleDownload}>
          <FaPlay />
        </button>
      )}
      {isDownloading && <p>Video yukleniyor...</p>}
      {videoUrl && isAnalyzing && <p>Mactaki olaylar tespit ediliyor...</p>}
      {videoUrl && !isAnalyzing && (
        <div className="videoContainer">
          <h4 className='match-name-playing'>{selectedMatch}</h4>
          <video className="mac-video" src={videoUrl} controls autoPlay />
        </div>
      )}
    </div>
  );
};

export default App;
