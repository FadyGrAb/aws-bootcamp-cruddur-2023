import './FormErrors.css';
import FormErrorItem from 'components/FormErrorItem';

export default function FormErrors(props) {
  let el_errors = null;
  if ((props.errors.length > 0) && Array.isArray(props.errors)) {
    el_errors = (<div className='errors'>
      {props.errors.map((err_code, key) => {
        return <FormErrorItem err_code={err_code} key={key}/>
      })}
    </div>)
  } else if (props.errors.length > 0) {
    el_errors = (<div className='errors'>
       <FormErrorItem err_code={props.errors} key={0}/>
    </div>)
  }

  return (
    <div className='errorsWrap'>
      {el_errors}
    </div>
  )
}