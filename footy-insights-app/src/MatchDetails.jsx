import React, { useState, useEffect } from 'react';
import './MatchDetails.css';

const MatchDetails = ({ link }) => {
  // const { sezon, hafta, takimlar } = details;
  const [details, setDetails] = useState(null);

  useEffect(() => {
    const fetchMatchDetails = async () => {
      try {
        const response = await fetch(link);
        if (!response.ok) throw new Error("JSON dosyası yüklenemedi!");
        const data = await response.json();
        setDetails(data);
      } catch (error) {
        console.error("Hata:", error);
      }
    };

    if (link) {
      fetchMatchDetails();
    }
  }, [link]);

  if (!details) {
    return <div>{link}</div>;
  }
  
  const { sezon, hafta, takimlar } = details;

    // Örnek: takim_1 ve takim_2
    const team1 = takimlar.takim_1;
    const team2 = takimlar.takim_2;
  
    const team1Name = team1.takimAdi[0];
    const team2Name = team2.takimAdi[0];
    const team1Score = team1.skor[0];
    const team2Score = team2.skor[0];
  
    const season = sezon[0];
    const week = hafta[0];

  return (
    <div className="match-details-container">
      <h2 className="match-title">
        {team1Name}  x  {team2Name}
      </h2>
      <p className="season-week">Sezon: {season}</p>
      <p className="season-week">Hafta: {week}</p>
      <p className="score">Skor: {team1Score} - {team2Score}</p>

      <div className="teams-wrapper">
        {/* Sol Takım */}
        <div className="team-block">
          <h3>{team1Name}</h3>

          <h4>İlk 11</h4>
          <ul>
            {team1.ilk11.map((player, idx) => (
              <li key={idx}>
                {player.oyuncuAdi} - {player.formaNo}
              </li>
            ))}
          </ul>

          {/* Devamı: yedekler, kartlar, goller, vb. */}

          <h4>Yedekler</h4>
          <ul>
            {team1.yedekler.map((player, idx) => (
              <li key={idx}>
                {player.oyuncuAdi} - {player.formaNo}
              </li>
            ))}
          </ul>

          <h4>Teknik Sorumlu</h4>
          {team1.teknikSorumlu}

          <h4>Kartlar</h4>
          <ul>
            {team1.kartlar.map((kart, idx) => (
              <li key={idx}>
                {kart.kartTuru} - {kart.dakika} - {kart.oyuncu} 
              </li>
            ))}
          </ul>

          <h4>Goller</h4>
          <ul>
            {team1.goller.map((gol, idx) => (
              <li key={idx}>
                {gol.dakika} - {gol.oyuncu} - {gol.golTipi}
              </li>
            ))}
          </ul>

          <h4>Oyundan Çıkanlar</h4>
          <ul>
            {team1.oyundanCikanlar.map((player, idx) => (
              <li key={idx}>
                {player.oyuncu} - {player.dakika}
              </li>
            ))}
          </ul>

          <h4>Oyuna Girenler</h4>
          <ul>
            {team1.oyunaGirenler.map((player, idx) => (
              <li key={idx}>
                {player.oyuncu} - {player.dakika}
              </li>
            ))}
          </ul>

        </div>

        {/* Sağ Takım */}
        <div className="team-block">
          <h3>{team2Name}</h3>

          <h4>İlk 11</h4>
          <ul>
            {team2.ilk11.map((player, idx) => (
              <li key={idx}>
                {player.oyuncuAdi} - {player.formaNo}
              </li>
            ))}
          </ul>

          {/* Devamı: yedekler, kartlar, goller, vb. */}

          <h4>Yedekler</h4>
          <ul>
            {team2.yedekler.map((player, idx) => (
              <li key={idx}>
                {player.oyuncuAdi} - {player.formaNo}
              </li>
            ))}
          </ul>

          <h4>Teknik Sorumlu</h4>
          {team1.teknikSorumlu}

          <h4>Kartlar</h4>
          <ul>
            {team2.kartlar.map((kart, idx) => (
              <li key={idx}>
                {kart.kartTuru} - {kart.dakika} - {kart.oyuncu} 
              </li>
            ))}
          </ul>

          <h4>Goller</h4>
          <ul>
            {team2.goller.map((gol, idx) => (
              <li key={idx}>
                {gol.dakika} - {gol.oyuncu} - {gol.golTipi}
              </li>
            ))}
          </ul>

          <h4>Oyundan Çıkanlar</h4>
          <ul>
            {team2.oyundanCikanlar.map((player, idx) => (
              <li key={idx}>
                {player.oyuncu} - {player.dakika}
              </li>
            ))}
          </ul>

          <h4>Oyuna Girenler</h4>
          <ul>
            {team2.oyunaGirenler.map((player, idx) => (
              <li key={idx}>
                {player.oyuncu} - {player.dakika}
              </li>
            ))}
          </ul>

        </div>
      </div>
    </div>
  );
};

export default MatchDetails;
