import './ActivityForm.css';
import React from "react";
import { useEffect, useState } from 'react';
import process from 'process';
import {ReactComponent as BombIcon} from './svg/bomb.svg';
import {post} from 'lib/Requests';
import FormErrors from 'components/FormErrors';
import ToxicityMeter from 'components/ToxicityMeter';

import * as toxicityClassifier from '@tensorflow-models/toxicity';

export default function ActivityForm(props) {
  const [count, setCount] = useState(0);
  const [message, setMessage] = useState('');
  const [ttl, setTtl] = useState('7-days');
  const [errors, setErrors] = useState([]);
  const [model, setModel] = useState(null);
  const [toxicity, setToxicity] = useState([]);

  const classes = []
  classes.push('count')
  if (240-count < 0){
    classes.push('err')
  }

  const onsubmit = async (event) => {
    event.preventDefault();
    const url = `${process.env.REACT_APP_BACKEND_URL}/api/activities`
    const payload_data = {
      message: message,
      ttl: ttl
    }
    post(url,payload_data,{
      auth: true,
      setErrors: setErrors,
      success: function(data){
        // add activity to the feed
        props.setActivities(current => [data,...current]);
        // reset and close the form
        setCount(0)
        setMessage('')
        setTtl('7-days')
        props.setPopped(false)
      }
  })
  }

  const textarea_onchange = async (event) => {
    setCount(event.target.value.length);
    setMessage(event.target.value);
    
    // toxicity detection
    const predictions = await model.classify([message]);
    setToxicity(predictions
      .filter(item => item.results[0].match === true)
      .map(item => item.label)
    );
      
  }

  const ttl_onchange = (event) => {
    setTtl(event.target.value);
  }

  // Load model
  useEffect(() => {
    async function loadModel() {
      const model = await toxicityClassifier.load(0.6);
      setModel(model);
    };
    if (model === null) {
      loadModel()
    };
    if (toxicity.length !== 0){
      setErrors(["Please be polite to be able to Crud!"]);
    } else {
      setErrors([]);
    }
  }, [model, message, toxicity])

  const disableButton = toxicity.length !== 0;

  if (props.popped === true) {
    return (
      <form 
        className='activity_form'
        onSubmit={onsubmit}
      >
        <textarea
          type="text"
          placeholder="what would you like to say?"
          value={message}
          onChange={textarea_onchange} 
          onBlur={textarea_onchange}
        />
        <div className='submit'>
          <div className={classes.join(' ')}>{240-count}</div>
          <button type='submit' disabled={disableButton} className={disableButton?"disabled":""}>Crud</button>
          <div className='expires_at_field'>
            <BombIcon className='icon' />
            <select
              value={ttl}
              onChange={ttl_onchange} 
            >
              <option value='30-days'>30 days</option>
              <option value='7-days'>7 days</option>
              <option value='3-days'>3 days</option>
              <option value='1-day'>1 day</option>
              <option value='12-hours'>12 hours</option>
              <option value='3-hours'>3 hours</option>
              <option value='1-hour'>1 hour </option>
            </select>
          </div>
        </div>
        <ToxicityMeter toxicity={toxicity} />
        <FormErrors errors={errors}/>
      </form>
    );
  }
}