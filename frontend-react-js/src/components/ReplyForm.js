import './ReplyForm.css';
import React from "react";
import { useEffect, useState } from 'react';
import process from 'process';
import {post} from 'lib/Requests';

import ActivityContent  from 'components/ActivityContent';
import FormErrors from 'components/FormErrors';

import ToxicityMeter from 'components/ToxicityMeter';

import * as toxicityClassifier from '@tensorflow-models/toxicity';

export default function ReplyForm(props) {
  const [count, setCount] = useState(0);
  const [message, setMessage] = useState('');
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
    const url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/${props.activity.uuid}/reply`
    const payload_data = {
      activity_uuid: props.activity.uuid,
      message: message
    }
    post(url,payload_data,{
      auth: true,
      setErrors: setErrors,
      success: function(data){
        if (props.setReplies) {
          props.setReplies(current => [data,...current]);
        }
        // reset and close the form
        setCount(0)
        setMessage('')
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

  let content;
  if (props.activity){
    content = <ActivityContent activity={props.activity} />;
  }

  const close = (event)=> {
    if (event.target.classList.contains("reply_popup")) {
      props.setPopped(false)
    }
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
      <div className="popup_form_wrap reply_popup" onClick={close}>
        <div className="popup_form">
          <div className="popup_heading">
            <div className="popup_title">
              Reply to...
            </div>
          </div>
          <div className="popup_content">
            <div className="activity_wrap">
              {content}
            </div>
            <form 
              className='replies_form'
              onSubmit={onsubmit}
            >
              <textarea
                type="text"
                placeholder="what is your reply?"
                value={message}
                onChange={textarea_onchange} 
                onBlur={textarea_onchange}
              />
              <div className='submit'>
                <div className={classes.join(' ')}>{240-count}</div>
                <button type='submit' disabled={disableButton} className={disableButton?"disabled":""}>Reply</button>
              </div>
              <ToxicityMeter toxicity={toxicity} />
              <FormErrors errors={errors} />
            </form>
          </div>
        </div>
      </div>
    );
  }
}