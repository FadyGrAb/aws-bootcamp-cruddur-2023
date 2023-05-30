import './ActivityItem.css';

import ActivityActionReply  from './ActivityActionReply';
import ActivityActionRepost  from './ActivityActionRepost';
import ActivityActionLike  from './ActivityActionLike';
import ActivityActionShare  from './ActivityActionShare';

import { Link } from "react-router-dom";
import { format_datetime, time_ago, time_future } from '../lib/DateTimeFormats';
import {ReactComponent as BombIcon} from './svg/bomb.svg';

export default function ActivityShowItem(props) {

  const attrs = {}
  attrs.className = 'activity_item expanded'

  const userIsAthenticated = localStorage.getItem("access_token") !== null;
  return (
    <div {...attrs}>
      <div className="acitivty_main">
        <div className='activity_content_wrap'>
          <div className='activity_content'>
            <Link className='activity_avatar'to={`/@`+props.activity.handle} ></Link>
            <div className='activity_meta'>
              <div className='activity_identity' >
                <Link className='display_name' to={`/@`+props.activity.handle}>{props.activity.display_name}</Link>
                <Link className="handle" to={`/@`+props.activity.handle}>@{props.activity.handle}</Link>
              </div>{/* activity_identity */}
              <div className='activity_times'>
                <div className="created_at" title={format_datetime(props.activity.created_at)}>
                  <span className='ago'>{time_ago(props.activity.created_at)}</span> 
                </div>
                <div className="expires_at" title={format_datetime(props.activity.expires_at)}>
                  <BombIcon className='icon' />
                  <span className='ago'>{time_future(props.activity.expires_at)}</span>
                </div>
              </div>{/* activity_times */}
            </div>{/* activity_meta */}
          </div>{/* activity_content */}
          <div className="message">{props.activity.message}</div>
        </div>

        <div className='expandedMeta'>
          <div className="created_at">
            {format_datetime(props.activity.created_at)}
          </div>
        </div>
        <div className="activity_actions" disabled={!userIsAthenticated}>
          <ActivityActionReply setReplyActivity={props.setReplyActivity} activity={props.activity} setPopped={props.setPopped} activity_uuid={props.activity.uuid} count={props.activity.replies_count}/>
          <ActivityActionRepost activity_uuid={props.activity.uuid} count={props.activity.reposts_count}/>
          <ActivityActionLike activity_uuid={props.activity.uuid} count={props.activity.likes_count}/>
          <ActivityActionShare activity_uuid={props.activity.uuid} />
        </div>
      </div>
    </div>
  )
}