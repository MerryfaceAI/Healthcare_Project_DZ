import React, { useEffect, useState } from 'react';
import { getCurrentUser, CurrentUser } from '../api/users';
import male from '@/assets/default-avatar-male.png';
import female from '@/assets/default-avatar-female.png';

interface Props {
  inTopBar?: boolean;
  mode?: string;
}

const UserProfileCard: React.FC<Props> = ({ inTopBar = false, mode }) => {
  const [user, setUser] = useState<CurrentUser | null>(null);

  useEffect(() => {
    getCurrentUser().then(setUser).catch(console.error);
  }, []);

  if (!user) {
    return (
      <div className={`flex items-center ${inTopBar ? '' : 'dashboard-card'} p-2`}>
        <div className="h-10 w-10 bg-gray-200 rounded-full animate-pulse" />
        {!inTopBar && (
          <div className="ml-4 space-y-1 flex-1">
            <div className="h-4 bg-gray-200 rounded w-1/2 animate-pulse" />
            <div className="h-3 bg-gray-200 rounded w-1/3 animate-pulse" />
          </div>
        )}
      </div>
    );
  }

  const { first_name, last_name, role, gender, avatar_url, tags = [] } = user;
  const fallback = gender === 'female' ? female : male;

  return (
    <div
      className={`flex items-center ${
        inTopBar ? 'space-x-3' : 'dashboard-card space-x-4 p-4'
      }`}
    >
      <img
        src={avatar_url || fallback}
        alt={`${first_name} ${last_name}`}
        className={`rounded-full ${
          inTopBar ? 'h-10 w-10' : 'h-12 w-12'
        } object-cover border-2 border-btn-primary`}
      />
      {!inTopBar && (
        <div className="flex-1">
          <h2 className="text-lg font-semibold text-card-fg">
            {first_name} {last_name}
          </h2>
          <p className="text-sm text-muted">{role}</p>
          <div className="mt-2 flex flex-wrap gap-1">
            {tags.map(tag => (
              <span
                key={tag}
                className="text-xs bg-btn-primary text-btn-primary-fg px-2 py-0.5 rounded-full"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default UserProfileCard;
