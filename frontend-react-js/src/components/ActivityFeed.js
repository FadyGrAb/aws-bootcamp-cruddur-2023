import "./ActivityFeed.css";
import ActivityItem from "./ActivityItem";

export default function ActivityFeed(props) {
  let content;
  if (props.activities.length === 0){
    content = <div className='activity_feed_primer'>
      <span>Nothing to see here yet</span>
    </div>
  } else {
    let items;
    if (props.showType === "notifications") {
      items = props.activities.map(activity => {
        return <ActivityItem setReplyActivity={props.setReplyActivity} setPopped={props.setPopped} key={activity.uuid} activity={activity} />
        })
    } else {
      items = props.activities.filter((activity) => (activity.reply_to_activity_uuid === null)).map(activity => {
        return  <ActivityItem setReplyActivity={props.setReplyActivity} setPopped={props.setPopped} key={activity.uuid} activity={activity} />
        })
    }
    content = <div className='activity_feed_collection'>
        {items} 
      
    </div>
  }


  return (<div>
    {content}
  </div>
  );
}