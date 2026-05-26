import React, { useEffect, useState } from 'react';
import './SamplePickerModal.css';

// Map category folder name → key trong t.diseases
const CATEGORY_TO_DISEASE_KEY = {
  'Atelectasis':        'Atelectasis',
  'Cardiomegaly':       'Cardiomegaly',
  'Consolidation':      'Consolidation',
  'Edema':              'Edema',
  'Effusion':           'Effusion',
  'Emphysema':          'Emphysema',
  'Fibrosis':           'Fibrosis',
  'Fracture':           'Fracture',
  'Hernia':             'Hernia',
  'Infiltration':       'Infiltration',
  'Lung_Opacity':       'Lung Opacity',
  'Mass':               'Mass',
  'No_Finding':         'No Finding',
  'Nodule':             'Nodule',
  'Pleural_Thickening': 'Pleural_Thickening',
  'Pneumonia':          'Pneumonia',
  'Pneumothorax':       'Pneumothorax',
};

export default function SamplePickerModal({ t, onSelect, onClose }) {
  const [samples, setSamples] = useState({});
  const [activeCategory, setActiveCategory] = useState(null);

  useEffect(() => {
    fetch('/test-samples')
      .then(r => r.json())
      .then(data => {
        setSamples(data);
        const first = Object.keys(data)[0];
        if (first) setActiveCategory(first);
      })
      .catch(() => {});
  }, []);

  const categories = Object.keys(samples);

  const getCategoryLabel = (cat) => {
    const key = CATEGORY_TO_DISEASE_KEY[cat];
    return (key && t.diseases?.[key]) || cat.replace(/_/g, ' ');
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-box" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <span>{t.samplePickerTitle}</span>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>

        <div className="modal-body">
          {/* Sidebar categories */}
          <div className="modal-sidebar">
            {categories.map(cat => (
              <button
                key={cat}
                className={`cat-btn ${activeCategory === cat ? 'active' : ''}`}
                onClick={() => setActiveCategory(cat)}
              >
                {getCategoryLabel(cat)}
              </button>
            ))}
          </div>

          {/* Image grid — dùng URL tương đối để proxy forward đúng */}
          <div className="modal-grid">
            {activeCategory && (samples[activeCategory] || []).map((url, i) => (
              <img
                key={i}
                src={url}
                alt={`${getCategoryLabel(activeCategory)} ${i + 1}`}
                className="sample-thumb"
                onClick={() => onSelect(url, `${getCategoryLabel(activeCategory)}_${i + 1}.png`)}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
