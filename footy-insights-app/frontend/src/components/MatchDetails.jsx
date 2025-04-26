import React, { useState, useEffect } from 'react';
import './MatchDetails.css';

const MatchDetails = ({ link }) => {
  const [details, setDetails] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        
        // public klasöründeki statik dosyayı al
        const url = link.startsWith('http')
          ? link
          : `${process.env.PUBLIC_URL}/${link}`;
        
        const res = await fetch(url);

        if (!res.ok) throw new Error('JSON yüklenemedi!');
        setDetails(await res.json());
      } catch (err) {
        console.error(err);
      }
    }
    if (link) fetchData();
  }, [link]);

  if (!details) return <div>Yükleniyor...</div>;

  const { sezon, hafta, takimlar } = details;
  const team1 = takimlar.takim_1;
  const team2 = takimlar.takim_2;
  const teams = [team1, team2];
  const names = teams.map(t => t.takimAdi[0]);
  const scores = teams.map(t => t.skor[0]);

  const sections = [
    { title: 'İlk 11',           key: 'ilk11',            isText: false },
    { title: 'Yedekler',         key: 'yedekler',         isText: false },
    { title: 'Teknik Sorumlu',   key: 'teknikSorumlu',    isText: true  },
    { title: 'Kartlar',          key: 'kartlar',          isText: false },
    { title: 'Goller',           key: 'goller',           isText: false },
    { title: 'Oyundan Çıkanlar', key: 'oyundanCikanlar',  isText: false },
    { title: 'Oyuna Girenler',   key: 'oyunaGirenler',    isText: false },
  ];

  return (
    <div className="match-details-container">
      <h2 className="match-title">
        {names[0]} x {names[1]}
      </h2>
      <p className="season-week">Sezon: {sezon[0]}</p>
      <p className="season-week">Hafta: {hafta[0]}</p>
      <p className="score">Skor: {scores[0]} - {scores[1]}</p>

      <div className="columns-header">
        {names.map((n, i) => <div key={i}>{n}</div>)}
      </div>

      <div className="sections-wrapper">
        {sections.map(({ title, key, isText }) => (
          <div className="section" key={key}>
            <h4 className="section-title">{title}</h4>
            <div className="section-content">
              {teams.map((team, idx) => (
                <div
                  className="section-col"
                  key={idx}
                  style={{ textAlign: isText ? 'center' : (idx === 1 ? 'right' : 'left') }}
                >
                  {isText
                    ? <p className="section-text">{team[key]}</p>
                    : <ul>
                        {team[key].map((item, i) => {
                          let prefix = '', text = '', suffix = '';
                          switch (key) {
                            case 'ilk11':
                            case 'yedekler':
                              prefix = item.formaNo;
                              text = item.oyuncuAdi;
                              break;
                            case 'kartlar':
                              prefix = item.dakika;
                              text = item.oyuncu;
                              suffix = item.kartTuru;
                              break;
                            case 'goller':
                              prefix = item.dakika;
                              text = item.oyuncu;
                              suffix = item.golTipi;
                              break;
                            case 'oyundanCikanlar':
                            case 'oyunaGirenler':
                              prefix = item.dakika;
                              text = item.oyuncu;
                              break;
                          }
                          const right = idx === 1;
                          return (
                            <li key={i}>
                              {!right && <span className="item-prefix-left">{prefix}</span>}
                              {!right && suffix && <span className="item-suffix-left">{suffix}</span>}
                              <span className="item-text">{text}</span>
                              {right && suffix && <span className="item-suffix-right">{suffix}</span>}
                              {right  && <span className="item-prefix-right">{prefix}</span>}
                            </li>
                          );
                        })}
                      </ul>
                  }
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MatchDetails;
