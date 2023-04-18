import './ProfileAvatar.css';

export default function ProfileAvatar(props) {
  var backgroundImage = "none"
  if (props.id != null) {
    backgroundImage = `url("https://assets.crudderme.click/avatars/${props.id}.jpg")`
  } 
  // console.log("ProfileAvatar", props)
  // console.log(backgroundImage)
  const styles = {
    backgroundImage: backgroundImage,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
  };

  return (
    <div 
      className="profile-avatar"
      style={styles}
    ></div>
  );
}