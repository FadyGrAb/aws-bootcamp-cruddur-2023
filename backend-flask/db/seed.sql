INSERT INTO public.users (display_name, handle, email, cognito_user_id)
VALUES
  ('Andrew Brown', 'andrewbrown' , 'brown@mail.com', 'MOCK'),
  ('Andrew Bayko', 'bayko' ,'bayko@mail.com', 'MOCK'),
  ('other fady', 'other_fady' ,'otherfady@mail.com', 'MOCK'),
  ('fady', 'fady' ,'fady@mail.com', 'MOCK'),
  ('Londo Mollari', 'londo', 'lmollari@centari.com','MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'fady' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  ),
  (
    (SELECT uuid from public.users WHERE users.handle = 'other_fady' LIMIT 1),
    'This is the other me!',
    current_timestamp + interval '10 day'
  )