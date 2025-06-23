// src/components/UserProfileCard.tsx
import React from 'react';
import defaultAvatarMale from '../assets/default-avatar-male.png';

export interface CurrentUser {
  first_name: string;
  last_name: string;
  role: string;
  avatar_url?: string;
  tags?: string[];
}

interface Props {
  mode: 'icon-only' | 'full';
  user: CurrentUser;
}

const UserProfileCard: React.FC<Props> = ({ mode, user }) => {
  const src = user.avatar_url || defaultAvatarMale;
  const size = mode === 'icon-only' ? 32 : 48;

  return (
    <div className={mode === 'full' ? 'profile-card' : ''} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
      <img
        src={src}
        alt={`${user.first_name} ${user.last_name}`}
        style={{
          width: size,
          height: size,
          borderRadius: '50%',
          objectFit: 'cover',
          border: '2px solid var(--btn-primary)',
        }}
      />
      {mode === 'full' && (
        <div>
          <div className="text-lg font-semibold">
            {user.first_name} {user.last_name}
          </div>
          <div className="text-sm text-muted">{user.role}</div>
          <div className="flex flex-wrap gap-1 mt-1">
            {user.tags?.map((t) => (
              <span key={t} className="text-xs bg-btn-primary text-white px-2 py-0.5 rounded">
                {t}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default UserProfileCard;
