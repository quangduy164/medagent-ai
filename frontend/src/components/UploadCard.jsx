import React from 'react';
import analyzeIcon from '../assets/analyze_icon.png';

export default function UploadCard({
  t, preview, file, loading, error, inputRef,
  onFileChange, onDrop, onAnalyze, onOpenSamples,
}) {
  return (
    <section className="card upload-card">
      <h2>{t.uploadTitle}</h2>
      <div
        className={`dropzone ${preview ? 'has-image' : ''}`}
        onClick={() => inputRef.current.click()}
        onDrop={onDrop}
        onDragOver={(e) => e.preventDefault()}
      >
        {preview
          ? <img src={preview} alt="preview" className="preview-img" />
          : <div className="dropzone-hint">
              <span className="drop-icon">📂</span>
              <p>{t.uploadHint} <u>{t.uploadClick}</u></p>
              <p className="hint-sub">{t.uploadSub}</p>
            </div>
        }
      </div>

      <input ref={inputRef} type="file" accept="image/*"
        style={{ display: 'none' }}
        onChange={onFileChange} />

      {/* Nút chọn ảnh mẫu */}
      <button className="btn-sample" onClick={onOpenSamples} type="button">
        {t.orChooseSample}
      </button>

      {file && <p className="filename">📄 {file.name}</p>}

      <button className="btn-analyze" onClick={onAnalyze} disabled={!file || loading}>
        {loading
          ? <><span className="spinner" /> {t.analyzing}</>
          : <>{t.analyzeBtn} <img src={analyzeIcon} alt="" className="btn-icon" /></>
        }
      </button>
      {error && <p className="error-msg">❌ {error}</p>}
    </section>
  );
}
