interface LogoProps {
  size?: number
  className?: string
}

export function Logo({ size = 32, className = '' }: LogoProps) {
  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <svg width={size} height={size} viewBox="0 0 40 40" fill="none">
        <path d="M20 4 L14 12 L26 12 Z" fill="#3d9d2b" />
        <path d="M20 6 L11 14 L29 14 Z" fill="#5eb64d" />
        <path d="M20 8 L15 15 L25 15 Z" fill="#94d187" />
        <ellipse cx="20" cy="26" rx="10" ry="12" fill="#f2b135" />
        <path d="M14 22 L26 22 M14 26 L26 26 M14 30 L26 30" stroke="#e69517"
              strokeWidth="1.2" opacity="0.6" />
      </svg>
      <span className="font-semibold text-brand-800 tracking-tight">
        AgriTraceBio
      </span>
    </div>
  )
}
