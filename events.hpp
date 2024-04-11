namespace sead {

template <typename T>
struct Vector3 {
   T x;
   T y;
   T z;
};

} // namespace sead

namespace as {

namespace HoldEvent {

   struct AtCollision{
      int AttackDirection;
      int AttackType;
   };

   struct ShieldAtCollision{
   };

   struct Ragdoll{
   };

   struct JstAvdRec{
   };

   struct AcceptInput{
   };

   struct Guard{
      int GuardDirection;
      bool IsNotGuardSlow;
   };

   struct AnmSeqCancel{
   };

   struct SwordCancel{
   };

   struct JumpCancel{
   };

   struct FailedCancel{
   };

   struct Trans{
      float Value;
   };

   struct Rotate{
      const char * Bone;
   };

   struct NoChangeAS{
   };

   struct NoChangeFaceAS{
   };

   struct NoCurveInputAS{
   };

   struct Noise{
   };

   struct AwarenessScale{
   };

   struct WeaponBlur{
   };

   struct ReleaseStirrupL{
   };

   struct ReleaseStirrupR{
   };

   struct ReleaseReinsL{
   };

   struct ReleaseReinsR{
   };

   struct NoFaceControll{
   };

   struct EyelidControl{
   };

   struct ModelInvisible{
   };

   struct PredictionShoot{
   };

   struct IK{
   };

   struct AnmGroup{
   };

   struct FixedMoveDirection{
   };

   struct OffTgSensorFilter{
   };

   struct OffHelperBone{
   };

   struct SpecialBoneControl{
   };

   struct Sync{
      int Value;
   };

   struct OffCloth{
   };

   struct NoFeedbackControl{
   };

   struct ChanceAttackAfter{
   };

   struct ShapeChange{
   };

   struct NoAutoAim{
   };

   struct KeepBoneControlAngle{
      const char * LookingController;
   };

   struct FreeMoving{
   };

   struct Lie{
   };

   struct NoSeFloorContact{
   };

   struct Slip{
   };

   struct ChangeGround{
   };

   struct EffectOn{
   };

   struct WeaponBreakFinish{
   };

   struct NoLegBendOnHorse{
   };

   struct ChangeSeFloorContact{
   };

   struct PreAttack{
   };

   struct ReleaseWeapon{
   };

   struct RumbleControllerHold{
      const char * Value;
   };

   struct HeadEquipNoDisplay{
   };

   struct ChangeForm{
   };

   struct RemovePartial{
   };

   struct FloorContact{
      const char * Bone;
      const char * GroundType;
      sead::Vector3<float> Velocity;
   };

   struct AcceptOneTouchBond{
   };

   struct JustGuard{
      int GuardDirection;
   };

   struct NoSpurs{
   };

   struct BurstPeriod{
   };

   struct DungeonBossZoraFinVisible{
   };

   struct DungeonBossZoraSharkFinVisible{
   };

   struct  LimitLookIK{
   };

   struct  Dodge{
   };

   struct GetOffBack{
   };

   struct OverrideReaction{
      int Key;
   };

   struct NoWeaponAbility{
   };

   struct InvalidAutoHeadLookIK{
   };

   struct BowCharge{
   };

   struct Rolling{
   };

   struct WeaponInvisible{
   };

   struct YunboAccessoryVisible{
   };

   struct MogurudoWaitEating{
   };

   struct DungeonBossGoronBreakableRoot{
   };

   struct ZonauGolemEyeLightOn{
   };

   struct MogurudoVacuum{
   };

   struct ZonauGolemEnableZonauParts{
   };

   struct Showing{
   };

   struct FixPlayerLookPos{
   };

   struct ForbidRagdoll{
   };

   struct DrakeDisableTailRagdoll{
   };

   struct ChangeGlideAnm{
   };

   struct DisableHandIK{
   };

   struct InvalidChangeGlideAnm{
   };

   struct AttachmentVisibleOn{
   };

   struct Spraining{
   };

   struct DisableBoneModifier{
   };

   struct ForbidJustAvoid{
   };

   struct LadderStepSync{
   };

   struct FittingModelToSlope{
   };

   struct HasToSyncRiderAnm{
   };

   struct DisableAIScheduleLOD{
   };

   struct NoBlinkChangeFaceEmotion{
   };

   struct DisableGuard{
   };

   struct LookIKReturn{
   };

   struct GuardBreak{
   };

   struct FootIK{
   };

} // namespace HoldEvent

namespace TriggerEvent {

   struct AtSound{
   };

   struct AttackCharge{
   };

   struct ObjThrow{
   };

   struct ObjGrab{
   };

   struct ObjPut{
   };

   struct WeaponDrawn{
      int Value;
   };

   struct WeaponHold{
      int Value;
   };

   struct Jump{
      float Value;
   };

   struct Break{
   };

   struct Face{
      const char * Value;
   };

   struct FaceTalk{
   };

   struct UpdateAtCol{
   };

   struct CrossFade{
   };

   struct EyeBlink{
   };

   struct EmitEffect{
   };

   struct OpenMessage{
   };

   struct Voice{
      const char * Value;
   };

   struct FireExtinguish{
   };

   struct GrabDelete{
   };

   struct StartFeedbackControl{
   };

   struct ParameterChange{
   };

   struct SheikahStoneGrab{
   };

   struct SheikahStonePut{
   };

   struct SheikahStoneGrabWaist{
   };

   struct SheikahStoneReturnWaist{
   };

   struct ResetBoneControl{
   };

   struct ResetWeatherChangedFlag{
   };

   struct ChangeSignal{
   };

   struct Flap{
      int Direction;
      float Velocity;
      const char * Bone;
   };

   struct UpdateHeartGauge{
   };

   struct Show{
   };

   struct RumbleControllerTrigger{
      const char * Value;
   };

   struct CameraReset{
   };

   struct FadeStart{
   };

   struct PlayerFace{
   };

   struct SpurKick{
   };

   struct ApproachStart{
   };

   struct NpcRitoTakeOff{
   };

   struct NpcRitoLanding{
   };

   struct ActivateWeaponAbility{
   };

   struct SheikahStoneGrabWaistRight{
   };

   struct ClimbEnd{
   };

   struct DecideAttackPos{
   };

   struct RequestZonauMaterial{
   };

   struct ActivateArmorAbility{
   };

   struct ChangableSprain{
   };

   struct DungeonGoronBossRestoreRLeg{
   };

   struct DungeonGoronBossRestoreLLeg{
   };

} // namespace TriggerEvent

} // namespace as