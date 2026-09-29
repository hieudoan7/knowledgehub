import type { LucideIcon } from "lucide-react";

type StatCardProps = {
    icon: LucideIcon
    label: string
    value: number
}

function StatCard({icon: Icon, label, value}: StatCardProps) {
    return (
        <div className="flex flex-1 flex-col gap-2 rounded-lg border border-border-default bg-surface-default p-4">
            <div className="flex items-center gap-2">
                <Icon className="h-5 w-5 text-text-secondary"/>
                <span className="text-base text-text-secondary">
                    {label}
                </span>
            </div>
            <span className="text-2xl font-semibold leading-8 text-text-primary">
                {value}
            </span>
        </div>
    )
}

export default StatCard