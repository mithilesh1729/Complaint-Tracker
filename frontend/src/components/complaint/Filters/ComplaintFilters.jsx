import FilterField from "./FilterField";

import "./ComplaintFilters.css";

function ComplaintFilters({
  filters,

  config,

  onChange,

  onRefresh,
}) {
  return (
    <div className="complaint-filters">
      <div className="filter-fields">
        {config.map((field) => (
          <FilterField
            key={field.key}
            field={field}
            value={filters[field.key]}
            onChange={(value) => {
              onChange({
                [field.key]: value,
              });
            }}
          />
        ))}
      </div>

      <button className="refresh-button" onClick={onRefresh}>
        Refresh
      </button>
    </div>
  );
}

export default ComplaintFilters;
