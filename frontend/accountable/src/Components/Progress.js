import './Progress.css';

function Progress(props) {
    let checked = props.checked;
    let total = props.total;
        
    return (
        <div className='progress'>
            <div className='progress-container'>
                <div className='progress-bar' style={{width: `${checked / total * 100}%`}}></div>
            </div>
            <p>{checked}/{total}</p>
        </div>
    );
}

export default Progress;