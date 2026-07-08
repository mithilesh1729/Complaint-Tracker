import AppLayout from "../../../components/layout/AppLayout";
import PageHeader from "../../../components/layout/PageHeader";
import Card from "../../../components/common/Card";

import ComplaintForm from "../../../components/complaint/ComplaintForm";

import "./RaiseComplaint.css";

function RaiseComplaint() {
  return (
    <>
      <div className="raise-complaint-page">
        <PageHeader
          title="Raise Complaint"
          subtitle="Submit your complaint with complete details."
        />

        <Card className="complaint-card">
          <ComplaintForm />
        </Card>
      </div>
    </>
  );
}

export default RaiseComplaint;
