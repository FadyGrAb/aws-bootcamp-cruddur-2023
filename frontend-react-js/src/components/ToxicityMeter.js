import './ToxicityMeter.css'

export default function ToxicityMeter(props){
    const meter = props.toxicity.map((item, key) => {
        return <div key={key} className='toxicity-item'>{item}</div>
    })

    let impression = null;
    switch(props.toxicity.length){
        case 1:
            impression = '🤨';
            break;
        case 2:
            impression = '🤔';
            break;
        case 3:
            impression = '😯';
            break;
        case 4:
            impression = '😠';
            break;
        case 5:
            impression = '😡';
            break;
        case 6:
            impression = '🤬';
            break;
        default:
            impression = '';
    }
    return (
        <div className="toxicity-wrapper">
            {impression}{meter}
        </div>
    )
}